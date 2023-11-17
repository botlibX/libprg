# This file is placed in the Public Domain.
#
# pylint: disable=C,R,W0201,W0212,W0105,W0613,W0406,W0611,E0102


"program"


import getpass
import os
import pwd
import readline
import sys
import termios
import time


from . import Censor, CLI, Commands, Default, Errors, Event, Storage
from . import cdir, command, forever, parse, lsmod, modules, scan


cfg = Default()
cfg.mod = ",".join((lsmod(modules.__path__[0])))
cfg.name    = "prg"
Storage.wd  = os.path.expanduser(f"~/.{cfg.name}")
cfg.pidfile = os.path.join(Storage.wd, f"{cfg.name}.pid")
cfg.user    = getpass.getuser()


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


def daemon(pidfile, verbose=False):
    pid = os.fork()
    if pid != 0:
        os._exit(0)
    os.setsid()
    pid2 = os.fork()
    if pid2 != 0:
        os._exit(0)
    if not verbose:
        with open('/dev/null', 'r', encoding="utf-8") as sis:
            os.dup2(sis.fileno(), sys.stdin.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as sos:
            os.dup2(sos.fileno(), sys.stdout.fileno())
        with open('/dev/null', 'a+', encoding="utf-8") as ses:
            os.dup2(ses.fileno(), sys.stderr.fileno())
    os.umask(0)
    os.chdir("/")
    if os.path.exists(pidfile):
        os.unlink(pidfile)
    cdir(os.path.dirname(pidfile))
    with open(pidfile, "w", encoding="utf-8") as fds:
        fds.write(str(os.getpid()))


def isop(txt):
    for char in txt:
        if char in cfg.opts:
            return True
    return False


def privileges(username):
    pwnam = pwd.getpwnam(username)
    os.setgid(pwnam.pw_gid)
    os.setuid(pwnam.pw_uid)


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
    wait = False
    if isop("d"):
        daemon(cfg.pidfile, isop("v"))
        privileges(cfg.user)
        wait = True
    cfg.mod = ",".join((lsmod(modules.__path__[0])))
    if isop("cd"):
        scan(modules, cfg.mod, not isop("x"), isop("w"))
    if isop("c"):
        csl = Console()
        if isop("t"):
            csl.threaded = True
        csl.start()
        wait = True
    if wait:
        forever()
        return
    scan(modules, cfg.mod)
    cli = CLI()
    command(cfg.otxt, cli)


def wrapped():
    wrap(main)
    Errors.show()


if __name__ == "__main__":
    wrapped()
        