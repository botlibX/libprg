# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0718


"repeaters"


import threading
import time


from .threads import Thread, launch


def __dir__():
    return (
        'Repeater',
        'Timer'
    )


__all__ = __dir__()
    

class Timer:

    def __init__(self, sleep, func, *args, thrname=None):
        ""
        self.args  = args
        self.func  = func
        self.sleep = sleep
        self.name  = thrname or str(self.func).split()[2]
        self.state = {}
        self.timer = None

    def run(self) -> None:
        ""
        self.state["latest"] = time.time()
        launch(self.func, *self.args)

    def start(self) -> None:
        ""
        timer = threading.Timer(self.sleep, self.run)
        timer.name   = self.name
        timer.daemon = True
        timer.sleep  = self.sleep
        timer.state  = self.state
        timer.func   = self.func
        timer.state["starttime"] = time.time()
        timer.state["latest"]    = time.time()
        timer.start()
        self.timer   = timer

    def stop(self) -> None:
        ""
        if self.timer:
            self.timer.cancel()


class Repeater(Timer):

    def run(self) -> Thread:
        ""
        thr = launch(self.start)
        super().run()
        return thr
