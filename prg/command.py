# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718


"commands"


import inspect


from .brokers import Broker
from .excepts import Errors
from .objects import Object
from .parsers import parse


def __dir__():
    return (
        'Commands',
    )


__all__ = __dir__()


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
