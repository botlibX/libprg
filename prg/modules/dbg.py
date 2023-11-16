# This file is placed in the Public Domain.
#
#


"tests"


class Test(Exception):

    pass


def dbg(event):
    event.reply("yooo!")
    raise Test()
