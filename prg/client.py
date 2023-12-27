# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0613


"client"


from .command import Command
from .group   import Group
from .handler import Handler


def __dir__():
    return (
         "Client",
    )


__all__ = __dir__()


class Client(Handler):

    def __init__(self):
        Handler.__init__(self)
        self.register("command", Command.handle)
        Group.add(self)

    def announce(self, txt):
        self.raw(txt)

    def say(self, channel, txt):
        self.raw(txt)

    def raw(self, txt):
        pass
