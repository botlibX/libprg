# This file is placed in the Public Domain.
#
# pylint: disable=C0116,E0402,E0401


"list of commands"


from ..run import CLI


"commands"


def cmd(event):
    event.reply(",".join(sorted(CLI.cmds)))
