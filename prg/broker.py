# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116


"brokering"


from .object import Object


"broker"


class Broker(Object):

    objs = []

    @staticmethod
    def add(obj) -> None:
        Broker.objs.append(obj)

    @staticmethod
    def announce(txt) -> None:
        for obj in Broker.objs:
            obj.announce(txt)

    @staticmethod
    def byorig(orig) -> Object:
        for obj in Broker.objs:
            if object.__repr__(obj) == orig:
                return obj
        return None

    @staticmethod
    def remove(obj) -> None:
        try:
            Broker.objs.remove(obj)
        except ValueError:
            pass

    @staticmethod
    def say(orig, channel, txt) -> None:
        bot = Broker.byorig(orig)
        if not bot:
            return
        bot.dosay(channel, txt)
