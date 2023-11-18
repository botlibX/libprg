# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,W0702,W0718,E1102


"runtime"


import queue
import threading
import time
import _thread


from .brokers import Broker
from .censors import Censor
from .command import Commands
from .excepts import Errors
from .message import Message
from .parsers import parse
from .objects import Default, Object
from .storage import Storage, spl
from .threads import forever, launch


def __dir__():
    return (
        'CLI',
        'Reactor',
        'command',
        'scan'
    )


__all__ = __dir__()


class Reactor(Object):

    def __init__(self):
        Object.__init__(self)
        self.cbs      = Object()
        self.queue    = queue.Queue()
        self.stopped  = threading.Event()
        self.threaded = True
        Broker.add(self)

    def dispatch(self, evt) -> None:
        func = getattr(self.cbs, evt.type, None)
        if not func:
            evt.ready()
            return
        if self.threaded:
            evt._thrs.append(launch(func, evt))
        else:
            try:
                func(evt)
            except Exception as ex:
                Errors.add(ex)

    def loop(self) -> None:
        while not self.stopped.is_set():
            try:
                self.dispatch(self.poll())
            except (KeyboardInterrupt, EOFError):
                _thread.interrupt_main()

    def poll(self):
        return self.queue.get()

    def put(self, evt) -> None:
        self.queue.put_nowait(evt)

    def register(self, typ, cbs) -> None:
        setattr(self.cbs, typ, cbs)

    def start(self) -> None:
        launch(self.loop)

    def stop(self) -> None:
        self.stopped.set()


class CLI(Reactor):

    def __init__(self):
        Reactor.__init__(self)
        self.register("command", Commands.dispatch)

    def announce(self, txt):
        pass

    def dispatch(self, evt):
        return Commands.dispatch(evt)

    def say(self, channel, txt):
        raise NotImplementedError("CLI.say")


def command(txt, clt=None):
    cli = clt or CLI()
    evn = Message()
    evn.orig = object.__repr__(cli)
    evn.txt = txt
    parse(evn)
    cli.dispatch(evn)
    evn.wait()
    return evn


def scan(pkg, mnames, init=False, wait=False) -> []:
    res = []
    if not pkg:
        return res
    for mname in spl(mnames):
        module = getattr(pkg, mname, None)
        if not module:
            continue
        Commands.scan(module)
        Storage.scan(module)
        res.append(module)
        if init and "init" in dir(module):
            module._thr = launch(module.init)
    if wait:
        for mod in res:
            if "_thr" not in dir(mod):
                continue
            mod._thr.join()
    return res
