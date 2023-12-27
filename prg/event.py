# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"event"


import threading


from .default import Default
from .group   import Group


def __dir__():
    return (
        'Event',
    )


__all__ = __dir__()


class Event(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self._thr    = None
        self.done    = False
        self.orig    = None
        self.result  = []
        self.txt     = ""

    def ready(self):
        self._ready.set()

    def reply(self, txt) -> None:
        self.result.append(txt)

    def show(self) -> None:
        for txt in self.result:
            bot = Group.byorig(self.orig) or Group.first()
            if bot:
                bot.say(self.channel, txt)

    def wait(self):
        if self._thr:
            self._thr.join()
        self._ready.wait()
        return self.result
