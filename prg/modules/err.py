# This file is placed in the Public Domain.
#
# pylint: disable=C0116,W0105,E0402


"status of bots"


from .. import Broker, Errors


DEBUG = False


def err(event):
    print(event)
    nmr = 0
    for bot in Broker.objs:
        if 'state' in dir(bot):
            event.reply(str(bot.state))
            nmr += 1
    if not nmr:
        event.reply("no status")
    if not Errors.errors:
        event.reply("no errors")
    if not DEBUG:
        for exc in Errors.errors:
            txt = Errors.format(exc)
            for line in txt.split():
                event.reply(line)
