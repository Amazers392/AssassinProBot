from telegram import ChatAction
import html
import urllib.request
import re
import json
from typing import Optional, List
import time
import urllib
from urllib.request import urlopen, urlretrieve
from urllib.parse import quote_plus, urlencode
import requests
from telegram import Message, Chat, Update, Bot, MessageEntity
from telegram import ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from assassin import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, DEV_USERS
from assassin.__main__ import STATS, USER_INFO
from assassin.modules.helper_funcs.filters import CustomFilters
from assassin.modules.disable import DisableAbleCommandHandler

def boobs(bot: Bot, update: Update):
    nsfw = requests.get('http://api.oboobs.ru/noise/1').json()[0]["preview"]
    final = "http://media.oboobs.ru/{}".format(nsfw)
    update.message.reply_photo(final)
    
def butts(bot: Bot, update: Update):
    nsfw = requests.get('http://api.obutts.ru/noise/1').json()[0]["preview"]
    final = "http://media.obutts.ru/{}".format(nsfw)
    update.message.reply_photo(final)
    
__help__ = """
Only For Sudos And Devs :)
- /boobs: Sends Random Boobs pic.
 - /butts: Sends Random Butts pic.
"""
__mod_name__ = "NSFW"

BOOBS_HANDLER = DisableAbleCommandHandler("boobs", boobs,
					  filters=CustomFilters.sudo_filter | CustomFilters.dev_filter)
BUTTS_HANDLER = DisableAbleCommandHandler("butts", butts,
                                          filters=CustomFilters.sudo_filter | CustomFilters.dev_filter)

dispatcher.add_handler(BOOBS_HANDLER)
dispatcher.add_handler(BUTTS_HANDLER)
