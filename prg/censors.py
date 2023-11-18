# This file is placed in the Public Domain.
#
# pylint: disable=C,R,E1102


"exceptions"


import io
import traceback


from .objects import Object


def __dir__():
    return (
        'Censor',
        'debug'
    )


__all__ = __dir__()


class Censor(Object):

    output = None
    words = []

    @staticmethod
    def skip(txt) -> bool:
        for skp in Censor.words:
            if skp in str(txt):
                return True
        return False


def debug(txt):
    if Censor.output and not Censor.skip(txt):
        Censor.output(txt)
