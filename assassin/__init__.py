import logging
import os
import sys

import telegram.ext as tg

#Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO)

LOGGER = logging.getLogger(__name__)

LOGGER.info("Starting assassin...")

#If Python version is < 3.6, stops the bot.
#If sys.version_info[0] < 3 or sys.version_info[1] < 6:
#    LOGGER.error("You MUST have a python version of at least 3.6! Multiple features depend on this. Bot quitting.")
#    quit(1)
    

from assassin.config import Development as Config
TOKEN = Config.API_KEY
try:
    OWNER_ID = int(Config.OWNER_ID)
except ValueError:
    raise Exception("Your OWNER_ID variable is not a valid integer.")

try:
    MESSAGE_DUMP = Config.MESSAGE_DUMP
except ValueError:
    raise Exception("Your MESSAGE_DUMP must be set.")

#MESSAGE_DUMP = Config.MESSAGE_DUMP
OWNER_USERNAME = Config.OWNER_USERNAME

try:
    SUDO_USERS = set(int(x) for x in Config.SUDO_USERS or [])
except ValueError:
    raise Exception("Your sudo users list does not contain valid integers.")

try:
    DEV_USERS = set(int(x) for x in Config.DEV_USERS or [])
except ValueError:
    raise Exception("Your developers list does not contain valid integers.")

try:
    SUPPORT_USERS = set(int(x) for x in Config.SUPPORT_USERS or [])
except ValueError:
    raise Exception("Your support users list does not contain valid integers.")

try:
    WHITELIST_USERS = set(int(x) for x in Config.WHITELIST_USERS or [])
except ValueError:
    raise Exception("Your whitelisted users list does not contain valid integers.")

try:
    SPAMMERS = set(int(x) for x  in Config.SPAMMERS or [])
except ValueError:
    raise Exception("Your spammers users list does not contain valid integers.")

WEBHOOK = Config.WEBHOOK
URL = Config.URL
PORT = Config.PORT
CERT_PATH = Config.CERT_PATH

DB_URI = Config.SQLALCHEMY_DATABASE_URI
LOAD = Config.LOAD
NO_LOAD = Config.NO_LOAD
DEL_CMDS = Config.DEL_CMDS
STRICT_ANTISPAM = Config.STRICT_ANTISPAM
GBAN_LOGS = Config.GBAN_LOGS
WORKERS = Config.WORKERS
BAN_STICKER = Config.BAN_STICKER
ALLOW_EXCL = Config.ALLOW_EXCL
MAPS_API = Config.MAPS_API
API_WEATHER = Config.API_OPENWEATHER
AI_API_KEY = Config.AI_API_KEY
SUPPORT_GROUP = Config.SUPPORT_GROUP
DEEPFRY_TOKEN = os.environ.get('DEEPFRY_TOKEN', "")

SUDO_USERS.add(OWNER_ID)
DEV_USERS.add(OWNER_ID)

updater = tg.Updater(TOKEN, workers=WORKERS)

dispatcher = updater.dispatcher

SUDO_USERS = list(SUDO_USERS)
DEV_USERS = list(DEV_USERS)
WHITELIST_USERS = list(WHITELIST_USERS)
SUPPORT_USERS = list(SUPPORT_USERS)
SPAMMERS = list(SPAMMERS)

# Load at end to ensure all prev variables have been set
from assassin.modules.helper_funcs.handlers import CustomCommandHandler, CustomRegexHandler

# make sure the regex handler can take extra kwargs
tg.RegexHandler = CustomRegexHandler

if ALLOW_EXCL:
    tg.CommandHandler = CustomCommandHandler
    
# Disable this (line 151) if you dont have a antispam script
try:
	from assassin.antispam import antispam_restrict_user, antispam_cek_user, detect_user
	antispam_module = True
except ModuleNotFoundError:
	antispam_module = False
	LOGGER.info("Note: Can't load antispam module. This is an optional.")

def spamfilters(text, user_id, chat_id, message):
	# If msg from self, return True
	if user_id == 1125785992:
		return False
	print("{} | {} | {} | {}".format(text, user_id, message.chat.title, chat_id))
	if antispam_module:
		parsing_date = time.mktime(message.date.timetuple())
		detecting = detect_user(user_id, chat_id, message, parsing_date)
		if detecting:
			return True
		antispam_restrict_user(user_id, parsing_date)
	if int(user_id) in SPAMMERS:
		print("This user is spammer!")
		return True
	else:
		return False
