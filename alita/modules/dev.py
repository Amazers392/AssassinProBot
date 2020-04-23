import os
import subprocess
import sys
from time import sleep
from typing import List

from telegram import Bot, Update, TelegramError
from telegram.ext import CommandHandler, run_async

from alita import dispatcher
from alita.modules.helper_funcs.chat_status import dev_plus


@dev_plus
@run_async
def gitpull(bot: Bot, update: Update):
    sent_msg = update.effective_message.reply_text("Pulling all changes from remote and then attempting to restart.")
    subprocess.Popen('git pull', stderr=subprocess.PIPE, shell=True)
    sent_msg_text = sent_msg.text + "\n\nChanges pulled...I guess.. Restarting in "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("Restarted.")

@run_async
@dev_plus
def restart(bot: Bot, update: Update):
    update.effective_message.reply_text("Starting a new instance and shutting down this one")

    os.system('restart.bat')
    os.execv('start.bat', sys.argv)


GITPULL_HANDLER = CommandHandler("gitpull", gitpull)
RESTART_HANDLER = CommandHandler("restart", restart)

dispatcher.add_handler(GITPULL_HANDLER)
dispatcher.add_handler(RESTART_HANDLER)

__mod_name__ = "Dev"
__handlers__ = [GITPULL_HANDLER, RESTART_HANDLER]
