# -*- coding: utf-8 -*-

import re

from mattermost_bot.bot import respond_to


@respond_to('(.*) added to the channel by (.*)', re.IGNORECASE)
def added_to_channel(message, myname, channel_admin):
    message.reply('Hi, %s. I am %s. Glad to join this channel :) ' % (channel_admin, myname))

added_to_channel.__doc__ = "Response when added to a channel"
