# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0212,W0702,W0718,E1102


"messages"


import threading


from .brokers import Broker
from .objects import Default


def __dir__():
    return (
        'Message',
    )


__all__ = __dir__()
        

class Message(Default):

    def __init__(self):
        Default.__init__(self)
        self._ready  = threading.Event()
        self._thrs   = []
        self.orig    = None
        self.result  = []
        self.txt     = ""

    def ready(self):
        self._ready.set()

    def reply(self, txt) -> None:
        self.result.append(txt)

    def show(self) -> None:
        for txt in self.result:
            Broker.say(self.orig, self.channel, txt)

    def wait(self):
        for thr in self._thrs:
            thr.join()
        self._ready.wait()
        return self.result
