#!/usr/bin/env python3
# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,C0209,C0413,W0201,R0903,W0212,E0402
# pylint: disable=W0105,R1710


"runtime"


import inspect
import os
import termios
import time
import _thread


from .errors import Errors
from .object import Default, Object, spl
from .disk   import Storage


def __dir__():
    return (
        'Cfg',
        'CLI',
        'Errors',
        'Event',
        'lsmod',
        'parse',
        'scan'
    )


"defines"


def debug(txt):
    if "v" in Cfg.opts:
        print(txt)


Cfg = Default()


"cli"


class CLI:

    cmds = Object()

    @staticmethod
    def add(func) -> None:
        setattr(CLI.cmds, func.__name__, func)

    @staticmethod
    def dispatch(evt) -> None:
        func = getattr(CLI.cmds, evt.cmd, None)
        if not func:
            return
        try:
            func(evt)
            evt.show()
        except Exception as exc:
            Errors.add(exc)

    @staticmethod
    def scan(mod) -> None:
        for key, cmd in inspect.getmembers(mod, inspect.isfunction):
            if key.startswith("cb"):
                continue
            if 'event' in cmd.__code__.co_varnames:
                CLI.add(cmd)


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self.result  = []
        self.txt     = ""

    def reply(self, txt) -> None:
        self.result.append(txt)

    def show(self) -> None:
        raise NotImplementedError("Event.show")


"utilties"


def forever():
    debug("running forever")
    while 1:
        try:
            time.sleep(1.0)
        except:
            _thread.interrupt_main()


def lsmod(path) -> []:
    if not os.path.exists(path):
        return {}
    for fnm in os.listdir(path):
        if not fnm.endswith(".py"):
            continue
        if fnm in ["__main__.py", "__init__.py"]:
            continue
        yield fnm[:-3]


def scan(pkg, mnames=None) -> []:
    if not pkg:
        return []
    if mnames is None:
        mnames = ",".join(lsmod(pkg.__path__[0]))
    for mname in spl(mnames):
        module = getattr(pkg, mname, None)
        if not module:
            continue
        CLI.scan(module)
        Storage.scan(module)


"methods"


def parse(obj, txt=None) -> None:
    args = []
    obj.args    = obj.args or []
    obj.cmd     = obj.cmd or ""
    obj.gets    = obj.gets or Default()
    obj.hasmods = obj.hasmod or False
    obj.index   = None
    obj.mod     = obj.mod or ""
    obj.opts    = obj.opts or ""
    obj.result  = obj.reult or []
    obj.sets    = obj.sets or Default()
    obj.otxt    = txt or obj.txt or ""
    _nr = -1
    for spli in obj.otxt.split():
        if spli.startswith("-"):
            try:
                obj.index = int(spli[1:])
            except ValueError:
                obj.opts += spli[1:]
            continue
        if "==" in spli:
            key, value = spli.split("==", maxsplit=1)
            if key in obj.gets:
                val = getattr(obj.gets, key)
                value = val + "," + value
            setattr(obj.gets, key, value)
            continue
        if "=" in spli:
            key, value = spli.split("=", maxsplit=1)
            if key == "mod":
                obj.hasmods = True
                if obj.mod:
                    obj.mod += f",{value}"
                else:
                    obj.mod = value
                continue
            setattr(obj.sets, key, value)
            continue
        _nr += 1
        if _nr == 0:
            obj.cmd = spli
            continue
        args.append(spli)
    if args:
        obj.args = args
        obj.txt  = obj.cmd or ""
        obj.rest = " ".join(obj.args)
        obj.txt  = obj.cmd + " " + obj.rest
    else:
        obj.txt = obj.cmd or ""
