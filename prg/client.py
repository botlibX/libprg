# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0613


"client"


import inspect
import time
import _thread


from .command import Command
from .event   import Event
from .fleet   import Fleet
from .find    import spl
from .handler import Handler
from .object  import Object
from .storage import Storage
from .thread  import launch


def __dir__():
    return (
         "Client",
         'cmnd',
         'forever',
         'scan'
    )


__all__ = __dir__()


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", Command.handle)
        Fleet.add(self)

    def announce(self, txt):
        self.raw(txt)

    def say(self, channel, txt):
        self.raw(txt)

    def raw(self, txt):
        pass


"utility"


def cmnd(txt):
    evn = Event()
    evn.txt = txt
    Command.handle(evn)
    evn.wait()
    return evn


def forever():
    while 1:
        try:
            time.sleep(1.0)
        except (KeyboardInterrupt, EOFError):
            _thread.interrupt_main()


def scan(pkg, modstr, initer=False, wait=True) -> []:
    mods = []
    for modname in spl(modstr):
        module = getattr(pkg, modname, None)
        if not module:
            continue
        for key, cmd in inspect.getmembers(module, inspect.isfunction):
            if 'event' in cmd.__code__.co_varnames:
                Command.add(cmd)
        for key, clz in inspect.getmembers(module, inspect.isclass):
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)
        if initer and "init" in dir(module):
            module._thr = launch(module.init, name=f"init {modname}")
            mods.append(module)
    if wait and initer:
        for mod in mods:
            mod._thr.join()
    return mods
