# This file is placed in the Public Domain.
#
# pylint: disable=E0402,C0116


"show errors"


from ..error import Errors


"command"


def err(event):
    if not Errors.errors:
        event.reply("no errors")
        return
    for exc in Errors.errors:
        event.reply(Errors.format(exc))
