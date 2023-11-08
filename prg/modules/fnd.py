# This file is placed in the Public Domain.
#
# pylint: disable=E0402,E0602,C0116,E0401,W0105


"locate"


import time


from ..objects import fmt, keys
from ..storage import Storage, find, fntime, laps


"command"


def fnd(event):
    if not event.rest:
        res = sorted([x.split('.')[-1].lower() for x in Storage.files()])
        if res:
            event.reply(",".join(res))
        return
    otype = event.args[0]
    args = []
    if event.gets:
        args.extend(keys(event.gets))
    if event.rest:
        args.extend(event.args[1:])
    if not args:
        args = None
    clz = Storage.long(otype)
    if "." not in clz:
        for fnm in Storage.files():
            claz = fnm.split(".")[-1]
            if otype == claz.lower():
                clz = fnm
    nmr = 0
    for fnm, obj in find(clz, event.gets, event.index):
        lap = laps(time.time() - fntime(fnm))
        event.reply(f"{str(nmr or event.index):4s} {lap:7s} {fmt(obj, args, plain=True):50s}")
        nmr += 1
    if not nmr:
        event.reply("no result")
