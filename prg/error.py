# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,E0402,R0903,E1102


"errors"


import io
import traceback


from .object import Object


"defines"


def __dir__():
    return (
        'Censor',
        'Errors',
        'debug'
    )


"censor"


class Censor(Object):

    output = None
    words = []

    @staticmethod
    def skip(txt) -> bool:
        for skp in Censor.words:
            if skp in str(txt):
                return True
        return False


"errors"


class Errors(Object):

    errors = []

    @staticmethod
    def add(exc) -> None:
        excp = exc.with_traceback(exc.__traceback__)
        Errors.errors.append(excp)

    @staticmethod
    def format(exc) -> str:
        res = ""
        stream = io.StringIO(
                             traceback.print_exception(
                                                       type(exc),
                                                       exc,
                                                       exc.__traceback__
                                                      )
                            )
        for line in stream.readlines():
            res += line + "\n"
        return res

    @staticmethod
    def handle(exc) -> None:
        if Censor.output:
            Censor.output(Errors.format(exc))

    @staticmethod
    def show() -> None:
        for exc in Errors.errors:
            Errors.handle(exc)


"utilities"


def debug(txt):
    if Censor.output and not Censor.skip(txt):
        Censor.output(txt)
