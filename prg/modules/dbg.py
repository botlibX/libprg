# This file is placed in the Public Domain.
#
# pylint: disable=C,R


"tests"


class Test(Exception):

    pass


def dbg(event):
    event.reply("yooo!")
    raise Test()
