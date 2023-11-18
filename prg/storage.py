# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0105,E0402


"storage"


import datetime
import inspect
import os
import pathlib
import time
import _thread


from .objects import Object, Default, dump, fqn, items, load, update


lock = _thread.allocate_lock()


def __dir__():
    return (
        'Storage',
        'cdir',
        'fetch',
        'find',
        'fns',
        'fntime',
        'laps',
        'last',
        'lsmod',
        'strip',
        'sync',
        'where'
    )


__all__ = __dir__()


class Storage(Object):

    classes = {}
    wd = ""

    @staticmethod
    def add(clz) -> None:
        if not clz:
            return
        name = str(clz).split()[1][1:-2]
        Storage.classes[name] = clz

    @staticmethod
    def files() -> []:
        return os.listdir(Storage.store())

    @staticmethod
    def long(name) -> str:
        split = name.split(".")[-1].lower()
        res = name
        for named in Storage.classes:
            if split in named.split(".")[-1].lower():
                res = named
                break
        if "." not in res:
            for fnm in Storage.files():
                claz = fnm.split(".")[-1]
                if fnm == claz.lower():
                    res = fnm
        return res

    @staticmethod
    def mods() -> str:
        pth =  Storage.path("mods")
        cdir(pth)
        return pth

    @staticmethod
    def path(pth) -> str:
        if not pth:
            pth = ""
        pth2 =  os.path.join(Storage.wd, pth)
        cdir(pth2)
        return pth2

    @staticmethod
    def store(pth="") -> str:
        pth = os.path.join(Storage.wd, "store", pth)
        pth2 = os.path.dirname(pth)
        cdir(pth2)
        return pth

    @staticmethod
    def scan(mod) -> None:
        for key, clz in inspect.getmembers(mod, inspect.isclass):
            if key.startswith("cb"):
                continue
            if not issubclass(clz, Object):
                continue
            Storage.add(clz)


def cdir(pth) -> None:
    pth = pathlib.Path(pth)
    os.makedirs(pth, exist_ok=True)


def find(mtc, selector=None, index=None) -> []:
    clz = Storage.long(mtc)
    nr = -1
    for fnm in sorted(fns(clz), key=fntime):
        obj = Default()
        fetch(obj, fnm)
        if '__deleted__' in obj:
            continue
        if selector and not search(obj, selector):
            continue
        nr += 1
        if index is not None and nr != int(index):
            continue
        yield (fnm, obj)


def fns(mtc) -> []:
    dname = ''
    pth = Storage.store(mtc)
    for rootdir, dirs, _files in os.walk(pth, topdown=False):
        if dirs:
            for dname in sorted(dirs):
                if dname.count('-') == 2:
                    ddd = os.path.join(rootdir, dname)
                    fls = sorted(os.listdir(ddd))
                    for fll in fls:
                        yield strip(os.path.join(ddd, fll))


def fntime(daystr) -> float:
    daystr = daystr.replace('_', ':')
    datestr = ' '.join(daystr.split(os.sep)[-2:])
    if '.' in datestr:
        datestr, rest = datestr.rsplit('.', 1)
    else:
        rest = ''
    timed = time.mktime(time.strptime(datestr, '%Y-%m-%d %H:%M:%S'))
    if rest:
        timed += float('.' + rest)
    return timed


def ident(obj) -> str:
    return os.path.join(
                        fqn(obj),
                        os.path.join(*str(datetime.datetime.now()).split())
                       )


def laps(seconds, short=True) -> str:
    txt = ""
    nsec = float(seconds)
    if nsec < 1:
        return f"{nsec:.2f}s"
    year = 365*24*60*60
    week = 7*24*60*60
    nday = 24*60*60
    hour = 60*60
    minute = 60
    years = int(nsec/year)
    nsec -= years*year
    weeks = int(nsec/week)
    nsec -= weeks*week
    nrdays = int(nsec/nday)
    nsec -= nrdays*nday
    hours = int(nsec/hour)
    nsec -= hours*hour
    minutes = int(nsec/minute)
    nsec -= int(minute*minutes)
    sec = int(nsec)
    if years:
        txt += f"{years}y"
    if weeks:
        nrdays += weeks * 7
    if nrdays:
        txt += f"{nrdays}d"
    if short and txt:
        return txt.strip()
    if hours:
        txt += f"{hours}h"
    if minutes:
        txt += f"{minutes}m"
    if sec:
        txt += f"{sec}s"
    txt = txt.strip()
    return txt


def lsmod(path) -> []:
    if not os.path.exists(path):
        return {}
    for fnm in os.listdir(path):
        if not fnm.endswith(".py"):
            continue
        if fnm in ["__main__.py", "__init__.py"]:
            continue
        yield fnm[:-3]


def spl(txt) -> []:
    try:
        res = txt.split(',')
    except (TypeError, ValueError):
        res = txt
    return [x for x in res if x]


def strip(pth, nmr=3) -> str:
    return os.sep.join(pth.split(os.sep)[-nmr:])


def where():
    res = "/"
    for name in __file__.split(os.sep):
        res = os.path.join(res, name)
        if name == "libobj":
            break
    return res


def fetch(obj, pth) -> None:
    pth2 = Storage.store(pth)
    read(obj, pth2)
    return strip(pth)


def last(obj, selector=None) -> None:
    if selector is None:
        selector = {}
    result = sorted(
                    find(fqn(obj), selector),
                    key=lambda x: fntime(x[0])
                   )
    if result:
        inp = result[-1]
        update(obj, inp[-1])
        return inp[0]


def read(obj, pth) -> None:
    with lock:
        with open(pth, 'r', encoding='utf-8') as ofile:
            update(obj, load(ofile))


def search(obj, selector) -> bool:
    res = False
    for key, value in items(selector):
        if key not in obj:
            res = False
            break
        for vval in spl(str(value)):
            val = getattr(obj, key, None)
            if str(vval).lower() in str(val).lower():
                res = True
            else:
                res = False
                break
    return res


def sync(obj, pth=None) -> str:
    if pth is None:
        pth = ident(obj)
    pth2 = Storage.store(pth)
    write(obj, pth2)
    return pth


def write(obj, pth) -> None:
    with lock:
        cdir(os.path.dirname(pth))
        with open(pth, 'w', encoding='utf-8') as ofile:
            dump(obj, ofile)
