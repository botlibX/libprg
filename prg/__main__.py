# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0212,W0105,W0613,W0406

"program"


import os
import readline
import sys
import termios
import time


from prg import Censor, CLI, Commands, Default, Errors, Event, Storage
from prg import command, forever, parse, lsmod, modules, scan


cfg = Default()
cfg.name = "prg"
Storage.wd = os.path.expanduser("~/.prg")


class CLI(CLI):

    def say(self, channel, txt):
        txt = txt.encode('utf-8', 'replace').decode()
        sys.stdout.write(txt)
        sys.stdout.write("\n")
        sys.stdout.flush()


class Console(CLI):


    def poll(self) -> Event:
        evt = Event()
        evt.orig = object.__repr__(self)
        evt.txt = input("> ")
        evt.type = "command"
        return evt


def isop(txt):
    for char in txt:
        if char in cfg.opts:
            return True
    return False


def wrap(func) -> None:
    old = None
    try:
        old = termios.tcgetattr(sys.stdin.fileno())
    except termios.error:
        pass
    try:
        func()
    except (EOFError, KeyboardInterrupt):
        print("")
        sys.stdout.flush()
    finally:
        if old:
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, old)


def main():
    parse(cfg, " ".join(sys.argv[1:]))
    if isop("v"):
        Censor.output = print
        dte = time.ctime(time.time()).replace("  ", " ")
        print(f"{cfg.name.upper()} started {cfg.opts.upper()} started {dte}")
    cfg.mod = ",".join((lsmod(modules.__path__[0])))
    if isop("c"):
        scan(modules, cfg.mod, not isop("x"), isop("w"))
        csl = Console()
        if isop("t"):
            csl.threaded = True
        csl.start()
        forever()
        return
    scan(modules, cfg.mod)
    cli = CLI()
    command(cfg.otxt, cli)


def wrapped():
    wrap(main)

if __name__ == "__main__":
    wrapped()
    Errors.show()
        