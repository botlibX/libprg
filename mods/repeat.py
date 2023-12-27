# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718


"repeating"


from prg.thread import Thread, launch


from .timer  import Timer


def __dir__():
    return (
        'Repeat',
    )


__all__ = __dir__()


class Repeat(Timer):

    def run(self) -> Thread:
        thr = launch(self.start)
        super().run()
        return thr
