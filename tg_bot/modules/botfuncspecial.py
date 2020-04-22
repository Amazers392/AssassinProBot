import socket
import random
from io import BytesIO
from time import sleep
from typing import Optional, List
from telegram import TelegramError, Chat, Message
from telegram import Update, Bot, User
from telegram import ParseMode
from telegram.error import BadRequest
from telegram.ext import MessageHandler, Filters, CommandHandler
from telegram.ext.dispatcher import run_async
from telegram.utils.helpers import escape_markdown
from tg_bot.modules.helper_funcs.chat_status import is_user_ban_protected, user_admin, bot_admin, dev_plus, sudo_plus
import tg_bot.modules.sql.users_sql as sql
from tg_bot import dispatcher, OWNER_ID, SUDO_USERS, SUPPORT_USERS, LOGGER, DEV_USERS
from tg_bot.modules.helper_funcs.filters import CustomFilters
from tg_bot.modules.disable import DisableAbleCommandHandler

USERS_GROUP = 4

@run_async
@dev_plus
def botip(bot, update):
    ip_list = socket.gethostbyname_ex(socket.gethostname())
    num = 1
    ips = ip_list[2]
    textmsg = f"<b>Bot IP Information</b>\n\n<b>Hostname:</b> {ip_list[0]}\n<b>IP {num}</b>: {ips[0]}"
    for i in range(len(ips)):
        num += 1
        textmsg += f"\n<b>IP {num}:</b> {ips[i]}"

    bot.send_message(chat_id=update.message.chat_id, text=textmsg, parse_mode=ParseMode.HTML)

@run_async
@sudo_plus
def quickscope(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = str(args[1])
        to_kick = str(args[0])
    else:
        update.effective_message.reply_text("You don't seem to be referring to a chat/user")
    try:
        bot.kick_chat_member(chat_id, to_kick)
        update.effective_message.reply_text("Attempted banning " + to_kick + " from" + chat_id)
    except BadRequest as excp:
        update.effective_message.reply_text(excp.message + " " + to_kick)


@run_async
@sudo_plus
def quickunban(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = str(args[1])
        to_kick = str(args[0])
    else:
        update.effective_message.reply_text("You don't seem to be referring to a chat/user")
    try:
        bot.unban_chat_member(chat_id, to_kick)
        update.effective_message.reply_text("Attempted unbanning " + to_kick + " from" + chat_id)
    except BadRequest as excp:
        update.effective_message.reply_text(excp.message + " " + to_kick)


@run_async
@sudo_plus
def banall(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = str(args[0])
        all_mems = sql.get_chat_members(chat_id)
    else:
        chat_id = str(update.effective_chat.id)
        all_mems = sql.get_chat_members(chat_id)
    for mems in all_mems:
        try:
            bot.kick_chat_member(chat_id, mems.user)
            update.effective_message.reply_text("Tried banning " + str(mems.user))
            sleep(0.1)
        except BadRequest as excp:
            update.effective_message.reply_text(excp.message + " " + str(mems.user))
            continue


@run_async
@sudo_plus
def snipe(bot: Bot, update: Update, args: List[str]):
    try:
        chat_id = str(args[0])
        del args[0]
    except TypeError as excp:
        update.effective_message.reply_text("Please give me a chat to echo to!")
    to_send = " ".join(args)
    if len(to_send) >= 2:
        try:
            bot.sendMessage(int(chat_id), str(to_send))
        except TelegramError:
            LOGGER.warning("Couldn't send to group %s", str(chat_id))
            update.effective_message.reply_text("Couldn't send the message. Perhaps I'm not part of that group?")

@run_async
@dev_plus
def getlink(bot: Bot, update: Update, args: List[int]):
    if args:
        chat_id = int(args[0])
    else:
        update.effective_message.reply_text("You don't seem to be referring to a chat")
    for chat_id in args:
        try:
            chat = bot.getChat(chat_id)
            bot_member = chat.get_member(bot.id)
            if bot_member.can_invite_users:
                invitelink = bot.exportChatInviteLink(chat_id)
                update.effective_message.reply_text("Invite link for: " + chat_id + "\n" + invitelink)
            else:
                update.effective_message.reply_text("I don't have access to the invite link.")
        except BadRequest as excp:
                update.effective_message.reply_text(excp.message + " " + str(chat_id))
        except TelegramError as excp:
                update.effective_message.reply_text(excp.message + " " + str(chat_id))


SNIPE_HANDLER = CommandHandler("snipe", snipe, pass_args=True)
BANALL_HANDLER = CommandHandler("banall", banall, pass_args=True)
GETLINK_HANDLER = CommandHandler("getlink", getlink, pass_args=True)
QUICKSCOPE_HANDLER = CommandHandler(["quickscope", "quickban"], quickscope, pass_args=True)
QUICKUNBAN_HANDLER = CommandHandler(["quickunban", "quickunscope"], quickunban, pass_args=True)
BOTIP_HANDLER = CommandHandler("botip", botip)

dispatcher.add_handler(SNIPE_HANDLER)
dispatcher.add_handler(BANALL_HANDLER)
dispatcher.add_handler(QUICKSCOPE_HANDLER)
dispatcher.add_handler(QUICKUNBAN_HANDLER)
dispatcher.add_handler(GETLINK_HANDLER)
dispatcher.add_handler(BOTIP_HANDLER)

__mod_name__ = "Bot Staff Special"
__handlers__ = [SNIPE_HANDLER, GETLINK_HANDLER, QUICKSCOPE_HANDLER, QUICKUNBAN_HANDLER, BOTIP_HANDLER]
