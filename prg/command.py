# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718


"command"


import _thread


from .error  import Error
from .object import Object
from .parse  import parse_command


def __dir__():
    return (
        'Command',
    )


__all__ = __dir__()


lock = _thread.allocate_lock()


class Command(Object):

    cmds = Object()

    @staticmethod
    def add(func) -> None:
        setattr(Command.cmds, func.__name__, func)

    @staticmethod
    def handle(evt):
        parse_command(evt)
        func = getattr(Command.cmds, evt.cmd, None)
        if func:
            try:
                func(evt)
                evt.show()
            except Exception as exc:
                Error.add(exc)
        evt.ready()
