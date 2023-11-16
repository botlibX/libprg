# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,E0402,W0105 W0718,W0702,E1102,W0246


"errors"


import io
import traceback


from .object import Object


class Censor(Object):

    output = None
    words = []

    @staticmethod
    def skip(txt) -> bool:
        for skp in Censor.words:
            if skp in str(txt):
                return True
        return False


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


def debug(txt):
    if Censor.output and not Censor.skip(txt):
        Censor.output(txt)
