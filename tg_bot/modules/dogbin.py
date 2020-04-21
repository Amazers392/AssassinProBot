import html
import json
import random

from typing import Optional, List

import requests
from telegram import Message, Chat, Update, Bot, MessageEntity, ParseMode
from telegram.ext import CommandHandler, run_async, Filters
from telegram.utils.helpers import escape_markdown

from tg_bot import dispatcher
from tg_bot.modules.disable import DisableAbleCommandHandler

BASE_URL = 'https://del.dog'

@run_async
def paste(bot: Bot, update: Update, args: List[str]):
    message = update.effective_message

    if message.reply_to_message:
        data = message.reply_to_message.text
    elif len(args) >= 1:
        data = message.text.split(None, 1)[1]
    else:
        message.reply_text("What am I supposed to do with this?!")
        return

    r = requests.post(f'{BASE_URL}/documents', data=data.encode('utf-8'))

    if r.status_code == 404:
        update.effective_message.reply_text('Failed to reach dogbin')
        r.raise_for_status()

    res = r.json()

    if r.status_code != 200:
        update.effective_message.reply_text(res['message'])
        r.raise_for_status()

    key = res['key']
    if res['isUrl']:
        reply = f'Shortened URL: {BASE_URL}/{key}\nYou can view stats, etc. [here]({BASE_URL}/v/{key})'
    else:
        reply = f'{BASE_URL}/{key}'
    update.effective_message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)


__help__ = """
 - /paste: Create a paste or a shortened url using [dogbin](https://del.dog)
"""

__mod_name__ = "Dogbin"

PASTE_HANDLER = DisableAbleCommandHandler("paste", paste, pass_args=True)

dispatcher.add_handler(PASTE_HANDLER)
