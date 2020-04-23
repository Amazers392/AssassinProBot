import logging
import os
import sys
import time
import telegram.ext as tg

StartTime = time.time()

# enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

#if version < 3.6, stop bot.
if sys.version_info[0] < 3 or sys.version_info[1] < 7:
    LOGGER.error("You MUST have a python version of at least 3.7! Multiple features depend on this. Bot quitting.")
    quit(1)

from alita.config import Development as Config
TOKEN = Config.API_KEY
try:
    OWNER_ID = int(Config.OWNER_ID)
except ValueError:
    raise Exception("Your OWNER_ID variable is not a valid integer.")

try:
    MESSAGE_DUMP = Config.MESSAGE_DUMP
except ValueError:
    raise Exception("Your MESSAGE_DUMP must be set.")

OWNER_USERNAME = Config.OWNER_USERNAME

try:
    SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
except ValueError:
    raise Exception("Your sudo or dev users list does not contain valid integers.")

try:
    DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
except ValueError:
    raise Exception("Your sudo or dev users list does not contain valid integers.")

try:
    SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
except ValueError:
    raise Exception("Your support users list does not contain valid integers.")

try:
    WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
except ValueError:
    raise Exception("Your whitelisted users list does not contain valid integers.")

#Variables from Config.py
GBAN_LOGS = Config.GBAN_LOGS
WEBHOOK = Config.WEBHOOK
URL = Config.URL
PORT = Config.PORT
CERT_PATH = Config.CERT_PATH
DB_URI = Config.SQLALCHEMY_DATABASE_URI
LOAD = Config.LOAD
NO_LOAD = Config.NO_LOAD
DEL_CMDS = Config.DEL_CMDS
WORKERS = Config.WORKERS
BAN_STICKER = Config.BAN_STICKER
ALLOW_EXCL = Config.ALLOW_EXCL
CASH_API_KEY = Config.CASH_API_KEY
TIME_API_KEY = Config.TIME_API_KEY
STRICT_GBAN = Config.STRICT_GBAN
STRICT_GMUTE = Config.STRICT_GMUTE
BAN_STICKER = Config.BAN_STICKER
AI_API_KEY = Config.AI_API_KEY
SUPPORT_GROUP = Config.SUPPORT_GROUP
SUPPORT_CHANNEL = Config.SUPPORT_CHANNEL


updater = tg.Updater(TOKEN, workers=WORKERS)

dispatcher = updater.dispatcher

SUDO_USERS = list(SUDO_USERS) + list(DEV_USERS)
DEV_USERS = list(DEV_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)

# Load at end to ensure all prev variables have been set
from alita.modules.helper_funcs.handlers import CustomCommandHandler, CustomRegexHandler, CustomMessageHandler

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler
tg.CommandHandler = CustomCommandHandler
tg.MessageHandler = CustomMessageHandler

def spamfilters(text, user_id, chat_id):
    #print("{} | {} | {}".format(text, user_id, chat_id))
    if int(user_id) in SPAMMERS:
        print("This user is a spammer!")
        return True
    else:
        return False
