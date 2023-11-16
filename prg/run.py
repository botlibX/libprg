# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,E0402,W0105 W0718,W0702,E1102,W0246


"runtime"


import inspect
import queue
import threading
import time
import _thread


from .disk   import Storage
from .error  import Errors
from .object import Default, Object
from .parse  import parse, spl
from .thread import launch


def __dir__():
    return (
        'Broker',
        'Censor',
        'Cfg',
        'Commands',
        'Config',
        'Errors',
        'Event',
        'Reactor',
        'command',
        'forever',
        'scan'
    )


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self._thrs   = []
        self.orig    = None
        self.result  = []
        self.txt     = ""

    def ready(self):
        self._ready.set()

    def reply(self, txt) -> None:
        self.result.append(txt)

    def show(self) -> None:
        for txt in self.result:
            Broker.say(self.orig, self.channel, txt)

    def wait(self):
        for thr in self._thrs:
            thr.join()
        self._ready.wait()
        return self.result


class Broker(Object):

    objs = []

    @staticmethod
    def add(obj) -> None:
        Broker.objs.append(obj)

    @staticmethod
    def announce(txt) -> None:
        for obj in Broker.objs:
            if "announce" in dir(obj):
                obj.announce(txt)

    @staticmethod
    def byorig(orig) -> Object:
        for obj in Broker.objs:
            if object.__repr__(obj) == orig:
                return obj
        return None

    @staticmethod
    def remove(obj) -> None:
        try:
            Broker.objs.remove(obj)
        except ValueError:
            pass

    @staticmethod
    def say(orig, channel, txt) -> None:
        bot = Broker.byorig(orig)
        if not bot:
            return
        bot.say(channel, txt)


class Commands(Object):

    cmds = Object()

    def __init__(self):
        Object.__init__(self)
        Broker.add(self)

    @staticmethod
    def add(func) -> None:
        setattr(Commands.cmds, func.__name__, func)

    def announce(self, txt):
        pass

    @staticmethod
    def dispatch(evt) -> None:
        parse(evt)
        func = getattr(Commands.cmds, evt.cmd, None)
        if not func:
            evt.ready()
            return
        try:
            func(evt)
            evt.show()
        except Exception as exc:
            Errors.add(exc)
        evt.ready()
 
    def say(self, txt):
        raise NotImplementedError("Commands.say")

    @staticmethod
    def scan(mod) -> None:
        for key, cmd in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmd.__code__.co_varnames:
                Commands.add(cmd)


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

    def poll(self) -> Event:
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
    evn = Event()
    evn.orig = object.__repr__(cli)
    evn.txt = txt
    parse(evn)
    cli.dispatch(evn)
    evn.wait()
    return evn


def forever():
    while 1:
        try:
            time.sleep(1.0)
        except:
            _thread.interrupt_main()


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
