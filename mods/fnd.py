# This file is placed in the Public Domain.
#
# pylint: disable=E0402,E0602,C0116


"locate"


from prg.object import fmt
from prg.disk   import Storage
from prg.find   import find


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
    clz = Storage.long(otype)
    if "." not in clz:
        for fnm in Storage.files():
            claz = fnm.split(".")[-1]
            if otype == claz.lower():
                clz = fnm
    nmr = 0
    for fnm, obj in find(clz, event.gets):
        event.reply(f"{nmr} {fmt(obj, args, plain=True)}")
        nmr += 1
    if not nmr:
        event.reply("no result")
