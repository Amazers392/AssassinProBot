import html
import json
import html
import os
from typing import List, Optional

from telegram import Bot, Update, ParseMode, TelegramError
from telegram.ext import CommandHandler, run_async
from telegram.utils.helpers import mention_html

from assassin import dispatcher, WHITELIST_USERS, SUPPORT_USERS, SUDO_USERS, DEV_USERS, OWNER_ID
from assassin.modules.helper_funcs.chat_status import whitelist_user, dev_user
from assassin.modules.helper_funcs.extraction import extract_user
from assassin.modules.log_channel import loggable

ELEVATED_USERS_FILE = os.path.join(os.getcwd(), 'alita/elevated_users.json')


def check_user_id(user_id: int, bot: Bot) -> Optional[str]:
    if not user_id:
        reply = "That...is a chat!"

    elif user_id == bot.id:
        reply = "This does not work that way."

    else:
        reply = None
    return reply


@run_async
@dev_user
@loggable
def addsudo(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        message.reply_text("This member is already a Sudo User")
        return ""

    if user_id in SUPPORT_USERS:
        rt += "This user is already a Support User, Promoting to Sudo User."
        data['supports'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        rt += "This user is already a Whitelisted User, Promoting to Sudo User."
        data['whitelists'].remove(user_id)
        WHITELIST_USERS.remove(user_id)

    data['sudos'].append(user_id)
    SUDO_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + "\nSuccessfully set Disaster level of {} to Sudo User!".format(user_member.first_name))

    log_message = (f"#SUDO\n"
                   f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                   f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_user
@loggable
def addsupport(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        rt += "Demoting status of this Sudo User to Support User."
        data['sudos'].remove(user_id)
        SUDO_USERS.remove(user_id)

    if user_id in SUPPORT_USERS:
        message.reply_text("This user is already a Support User.")
        return ""

    if user_id in WHITELIST_USERS:
        rt += "Promoting Disaster level from Whitelist User to Support User."
        data['whitelists'].remove(user_id)
        WHITELIST_USERS.remove(user_id)

    data['supports'].append(user_id)
    SUPPORT_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(rt + f"\n{user_member.first_name} was added as a Support User!")

    log_message = (f"#SUPPORT\n"
                   f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                   f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_user
@loggable
def addwhitelist(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)
    rt = ""

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        rt += "This member is a Sudo User, Demoting to Whitelist User."
        data['sudos'].remove(user_id)
        SUDO_USERS.remove(user_id)

    if user_id in SUPPORT_USERS:
        rt += "This user is already a Support User, Demoting to Whitelist User."
        data['supports'].remove(user_id)
        SUPPORT_USERS.remove(user_id)

    if user_id in WHITELIST_USERS:
        message.reply_text("This user is already a Whitelisted User.")
        return ""

    data['whitelists'].append(user_id)
    WHITELIST_USERS.append(user_id)

    with open(ELEVATED_USERS_FILE, 'w') as outfile:
        json.dump(data, outfile, indent=4)

    update.effective_message.reply_text(
        rt + f"\nSuccessfully promoted {user_member.first_name} to a Whitelisted User!")

    log_message = (f"#WHITELIST\n"
                   f"<b>Admin:</b> {mention_html(user.id, user.first_name)} \n"
                   f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

    if chat.type != 'private':
        log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

    return log_message


@run_async
@dev_user
@loggable
def removesudo(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUDO_USERS:
        message.reply_text("Demoting to normal user")
        SUDO_USERS.remove(user_id)
        data['sudos'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (f"#UNSUDO\n"
                       f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                       f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

        if chat.type != 'private':
            log_message = "<b>{}:</b>\n".format(html.escape(chat.title)) + log_message

        return log_message

    else:
        message.reply_text("This user is not a Sudo!")
        return ""


@run_async
@dev_user
@loggable
def removesupport(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in SUPPORT_USERS:
        message.reply_text("Demoting to Civilian")
        SUPPORT_USERS.remove(user_id)
        data['supports'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (f"#UNSUPPORT\n"
                       f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                       f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message

    else:
        message.reply_text("This user is not a Support User!")
        return ""


@run_async
@dev_user
@loggable
def removewhitelist(bot: Bot, update: Update, args: List[str]) -> str:
    message = update.effective_message
    user = update.effective_user
    chat = update.effective_chat

    user_id = extract_user(message, args)
    user_member = bot.getChat(user_id)

    reply = check_user_id(user_id, bot)
    if reply:
        message.reply_text(reply)
        return ""

    with open(ELEVATED_USERS_FILE, 'r') as infile:
        data = json.load(infile)

    if user_id in WHITELIST_USERS:
        message.reply_text("Demoting to normal user")
        WHITELIST_USERS.remove(user_id)
        data['whitelists'].remove(user_id)

        with open(ELEVATED_USERS_FILE, 'w') as outfile:
            json.dump(data, outfile, indent=4)

        log_message = (f"#UNWHITELIST\n"
                       f"<b>Admin:</b> {mention_html(user.id, user.first_name)}\n"
                       f"<b>User:</b> {mention_html(user_member.id, user_member.first_name)}")

        if chat.type != 'private':
            log_message = f"<b>{html.escape(chat.title)}:</b>\n" + log_message

        return log_message
    else:
        message.reply_text("This user is not a Whitelisted User!")
        return ""


@run_async
@dev_user
def whitelistlist(bot: Bot, update: Update):
    reply = "<b>Whitelisted Users 🐺:</b>\n"
    for each_user in WHITELIST_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)

            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@dev_user
def supportlist(bot: Bot, update: Update):
    reply = "<b>Support Users 👹:</b>\n"
    for each_user in SUPPORT_USERS:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@dev_user
def sudolist(bot: Bot, update: Update):
    true_sudo = list(set(SUDO_USERS) - set(DEV_USERS))
    reply = "<b>Sudo Users 🐉:</b>\n"
    for each_user in true_sudo:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


@run_async
@dev_user
def devlist(bot: Bot, update: Update):
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply = "<b>Developers ⚡️:</b>\n"
    for each_user in true_dev:
        user_id = int(each_user)
        try:
            user = bot.get_chat(user_id)
            reply += f"• {mention_html(user_id, user.first_name)}\n"
        except TelegramError:
            pass
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)

@run_async
@dev_user
def botstaff(bot: Bot, update: Update):
    try:
        ownerbot = int(OWNER_ID)
        ownerid = bot.get_chat(ownerbot)
        reply = f"<b>🌟 Owner:</b> {mention_html(ownerbot, ownerid.first_name)}\n"
    except TelegramError:
        pass
    true_dev = list(set(DEV_USERS) - {OWNER_ID})
    reply += "\n<b>Developers⚡️:</b>\n"
    if true_dev == []:
        reply += "No Dev Users"
    else:
        for each_user in true_dev:
            user_id = int(each_user)
            try:
                user = bot.get_chat(user_id)
                reply += f"• {mention_html(user_id, user.first_name)}\n"
            except TelegramError:
                pass
    true_sudo = list(set(SUDO_USERS) - set(DEV_USERS))
    reply += "\n<b>Sudo Users🐉:</b>\n"
    if true_sudo == []:
        reply += "No Sudo Users"
    else:
        for each_user in true_sudo:
            user_id = int(each_user)
            try:
                user = bot.get_chat(user_id)
                reply += f"• {mention_html(user_id, user.first_name)}\n"
            except TelegramError:
                pass
    reply += "\n<b>Support Users👹:</b>\n"
    if SUPPORT_USERS == []:
        reply += "No Support Users"
    else:
        for each_user in SUPPORT_USERS:
            user_id = int(each_user)
            try:
                user = bot.get_chat(user_id)
                reply += f"• {mention_html(user_id, user.first_name)}\n"
            except TelegramError:
                pass
    reply += "\n<b>Whitelisted Users🐺:</b>\n"
    if WHITELIST_USERS == []:
        reply += "No Whitelisted Users"
    else:
        for each_user in WHITELIST_USERS:
            user_id = int(each_user)
            try:
                user = bot.get_chat(user_id)

                reply += f"• {mention_html(user_id, user.first_name)}\n"
            except TelegramError:
                pass
    reply += "\n\nFor Seprate lists:\n/slist - Sudo Users\n/supportlist - Support Users\n/whitelist - Whitelisted Users\n/devs - Developers\nAbove commands only available for devs"
    update.effective_message.reply_text(reply, parse_mode=ParseMode.HTML)


SUDO_HANDLER = CommandHandler("addsudo", addsudo, pass_args=True)
SUPPORT_HANDLER = CommandHandler("addsupport", addsupport, pass_args=True)
WHITELIST_HANDLER = CommandHandler("addwhitelist", addwhitelist, pass_args=True)
UNSUDO_HANDLER = CommandHandler("rmsudo", removesudo, pass_args=True)
UNSUPPORT_HANDLER = CommandHandler("rmsupport", removesupport, pass_args=True)
UNWHITELIST_HANDLER = CommandHandler("rmwhitelist", removewhitelist, pass_args=True)

WHITELISTLIST_HANDLER = CommandHandler("whitelist", whitelistlist)
SUPPORTLIST_HANDLER = CommandHandler("supportlist", supportlist)
SUDOLIST_HANDLER = CommandHandler("slist", sudolist)
DEVLIST_HANDLER = CommandHandler("devs", devlist)
BOTSTAFF_HANDLER = CommandHandler("botstaff", botstaff)

dispatcher.add_handler(SUDO_HANDLER)
dispatcher.add_handler(SUPPORT_HANDLER)
dispatcher.add_handler(WHITELIST_HANDLER)
dispatcher.add_handler(UNSUDO_HANDLER)
dispatcher.add_handler(UNSUPPORT_HANDLER)
dispatcher.add_handler(UNWHITELIST_HANDLER)

dispatcher.add_handler(WHITELISTLIST_HANDLER)
dispatcher.add_handler(SUPPORTLIST_HANDLER)
dispatcher.add_handler(SUDOLIST_HANDLER)
dispatcher.add_handler(DEVLIST_HANDLER)
dispatcher.add_handler(BOTSTAFF_HANDLER)
