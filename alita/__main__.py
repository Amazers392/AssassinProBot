import importlib
import re
from typing import Optional, List

from telegram import Bot, Update, ParseMode, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import Unauthorized, BadRequest, TimedOut, NetworkError, ChatMigrated, TelegramError
from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, Filters
from telegram.ext.dispatcher import run_async, DispatcherHandlerStop
from telegram.utils.helpers import escape_markdown

from alita import dispatcher, updater, TOKEN, WEBHOOK, OWNER_ID, CERT_PATH, PORT, URL, LOGGER, \
    ALLOW_EXCL, SUPPORT_CHANNEL, SUPPORT_GROUP, OWNER_USERNAME
# needed to dynamically load modules
# NOTE: Module order is not guaranteed, specify that in the config file!
from alita.modules import ALL_MODULES
from alita.modules.helper_funcs.chat_status import is_user_admin
from alita.modules.helper_funcs.misc import paginate_modules

PM_START_TEXT = """
This Bot has been shfted to @Lucifer\_ProBot
Click here to add the bot to your groups!
Add new bot by clicking button below
"""

HELP_STRINGS = """
This Bot has been shfted to @Lucifer\_ProBot
Click here to add the bot to your groups!
Add new bot by clicking button below
"""

DONATE_STRING = """Heya, glad to hear you wanna donate!
The Bot is hosted on Heroku Free Servers and it would be really helpful if \
you can donate my owner to upgrade the server for faster performance \
You can donate by contacting him!"
"""

IMPORTED = {}
MIGRATEABLE = []
HELPABLE = {}
STATS = []
USER_INFO = []
DATA_IMPORT = []
DATA_EXPORT = []
CHAT_SETTINGS = {}
USER_SETTINGS = {}

for module_name in ALL_MODULES:
    imported_module = importlib.import_module("alita.modules." + module_name)
    if not hasattr(imported_module, "__mod_name__"):
        imported_module.__mod_name__ = imported_module.__name__

    if not imported_module.__mod_name__.lower() in IMPORTED:
        IMPORTED[imported_module.__mod_name__.lower()] = imported_module
    else:
        raise Exception("Can't have two modules with the same name! Please change one")

    if hasattr(imported_module, "__help__") and imported_module.__help__:
        HELPABLE[imported_module.__mod_name__.lower()] = imported_module

    # Chats to migrate on chat_migrated events
    if hasattr(imported_module, "__migrate__"):
        MIGRATEABLE.append(imported_module)

    if hasattr(imported_module, "__stats__"):
        STATS.append(imported_module)

    if hasattr(imported_module, "__user_info__"):
        USER_INFO.append(imported_module)

    if hasattr(imported_module, "__import_data__"):
        DATA_IMPORT.append(imported_module)

    if hasattr(imported_module, "__export_data__"):
        DATA_EXPORT.append(imported_module)

    if hasattr(imported_module, "__chat_settings__"):
        CHAT_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

    if hasattr(imported_module, "__user_settings__"):
        USER_SETTINGS[imported_module.__mod_name__.lower()] = imported_module

@run_async
def start(bot: Bot, update: Update):
    keyboard = [[InlineKeyboardButton(text="🎉 Add Lucifer to your Group!", url="t.me/Lucifer_Probot?startgroup=true")]]
    update.effective_message.reply_text("This bot has been deprecated, use new bot @Lucifer\_ProBot\nThe new bot has all your prevoius data saved!", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode=ParseMode.MARKDOWN, disable_web_page_preview=True)


def main():
    start_handler = CommandHandler("start", start)
    help_handler = CommandHandler("help", start)
    settings_handler = CommandHandler("settings", start)
    donate_handler = CommandHandler("donate", start)

    dispatcher.add_handler(start_handler)
    dispatcher.add_handler(help_handler)
    dispatcher.add_handler(settings_handler)
    dispatcher.add_handler(donate_handler)

    # dispatcher.add_error_handler(error_callback)

    if WEBHOOK:
        LOGGER.info("Using webhooks.")
        updater.start_webhook(listen="127.0.0.1",
                              port=PORT,
                              url_path=TOKEN)

        if CERT_PATH:
            updater.bot.set_webhook(url=URL + TOKEN,
                                    certificate=open(CERT_PATH, 'rb'))
        else:
            updater.bot.set_webhook(url=URL + TOKEN)

    else:
        LOGGER.info("Using long polling.")
        updater.start_polling(timeout=15, read_latency=4)
        LOGGER.info("Group Bot Started Successfull ;)")
        LOGGER.info("Please wait upto 2 minutes for bot to work.")
    updater.idle()

if __name__ == '__main__':
    LOGGER.info("Successfully loaded modules: " + str(ALL_MODULES))
    main()
