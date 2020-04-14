import os
import subprocess
import sys
from time import sleep
from typing import List

from telegram import Bot, Update, TelegramError
from telegram.ext import CommandHandler, run_async

from tg_bot import dispatcher
from tg_bot.modules.helper_funcs.chat_status import dev_plus


@dev_plus
def updatebot(bot: Bot, update: Update):
  subprocess.Popen('git clone https://Dc5000:Div2521%23@github.com/Dc5000/HitmanAgent47_Bot')
  subprocess.Popen('cd HitmanAgen47_Bot')
  subprocess.Popen('git push origin master:deployed')
  
  
  sent_msg = update.effective_message.reply_text("Pulling all changes from remote and then attempting to restart.")
  sent_msg_text = sent_msg.text + "\n\nChanges pulled...I guess.. Restarting in "

    for i in reversed(range(5)):
        sent_msg.edit_text(sent_msg_text + str(i + 1))
        sleep(1)

    sent_msg.edit_text("Restarted.")
    
GITPULL_HANDLER = CommandHandler("updatebot", updatebot)
__handlers__ = [GITPULL_HANDLER]
