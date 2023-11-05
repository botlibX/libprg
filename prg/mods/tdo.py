# This file is placed in the Public Domain.
#
# pylint: disable=C0115,C0116,R0903,W0105,E0402,W0612,E0401


"todo list"


import time


from ..disk   import sync
from ..object import Object
from ..find   import find, fntime, laps


"todo"


class Todo(Object):

    def __init__(self):
        Object.__init__(self)
        self.txt = ''


"commands"


def dne(event):
    if not event.args:
        event.reply("dne <txt>")
        return
    selector = {'txt': event.args[0]}
    nmr = 0
    for fnm, obj in find('todo', selector):
        nmr += 1
        obj.__deleted__ = True
        sync(obj, fnm)
        event.reply('ok')
        break
    if not nmr:
        event.reply("nothing todo")


def tdo(event):
    if not event.rest:
        nmr = 0
        for fnm, obj in find('todo'):
            lap = laps(time.time()-fntime(fnm))
            event.reply(f'{nmr} {obj.txt} {lap}')
            nmr += 1
        if not nmr:
            event.reply("no todo")
        return
    obj = Todo()
    obj.txt = event.rest
    sync(obj)
    event.reply('ok')
