from time import sleep

from telegram import Bot, Update, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.error import BadRequest, Unauthorized
from telegram.ext import CommandHandler, CallbackQueryHandler, run_async

import alita.modules.sql.global_bans_sql as gban_sql
import alita.modules.sql.users_sql as user_sql
from alita import dispatcher, OWNER_ID, DEV_USERS
from alita.modules.helper_funcs.chat_status import dev_plus

def get_invalid_chats(bot: Bot, update: Update, remove: bool = False):
    chat_id = update.effective_chat.id
    chats = user_sql.get_all_chats()
    kicked_chats, progress = 0, 0
    chat_list = []
    progress_message = None

    for chat in chats:

        if ((100 * chats.index(chat)) / len(chats)) > progress:
            progress_bar = f"{progress}% completed in getting invalid chats."
            if progress_message:
                try:
                    bot.editMessageText(progress_bar, chat_id, progress_message.message_id)
                except:
                    pass
            else:
                progress_message = bot.sendMessage(chat_id, progress_bar)
            progress += 5

        cid = chat.chat_id
        sleep(0.1)
        try:
            bot.get_chat(cid, timeout=60)
        except (BadRequest, Unauthorized):
            kicked_chats += 1
            chat_list.append(cid)
        except:
            pass

    try:
        progress_message.delete()
    except:
        pass

    if not remove:
        return kicked_chats
    else:
        for muted_chat in chat_list:
            sleep(0.1)
            user_sql.rem_chat(muted_chat)
        return kicked_chats


def get_invalid_gban(bot: Bot, update: Update, remove: bool = False):
    banned = gban_sql.get_gban_list()
    ungbanned_users = 0
    ungban_list = []

    for user in banned:
        user_id = user["user_id"]
        sleep(0.1)
        try:
            bot.get_chat(user_id)
        except BadRequest:
            ungbanned_users += 1
            ungban_list.append(user_id)
        except:
            pass

    if not remove:
        return ungbanned_users
    else:
        for user_id in ungban_list:
            sleep(0.1)
            gban_sql.ungban_user(user_id)
        return ungbanned_users

def get_muted_chats(bot: Bot, update: Update, leave: bool = False):
    chat_id = update.effective_chat.id
    chats = user_sql.get_all_chats()
    muted_chats, progress = 0, 0
    chat_list = []
    progress_message = None

    for chat in chats:

        if ((100 * chats.index(chat)) / len(chats)) > progress:
            progress_bar = f"{progress}% completed in getting muted chats."
            if progress_message:
                try:
                    bot.editMessageText(progress_bar, chat_id, progress_message.message_id)
                except:
                    pass
            else:
                progress_message = bot.sendMessage(chat_id, progress_bar)
            progress += 5

        cid = chat.chat_id
        sleep(0.1)

        try:
            bot.send_chat_action(cid, "TYPING", timeout=60)
        except (BadRequest, Unauthorized):
            muted_chats += 1
            chat_list.append(cid)
        except:
            pass

    try:
        progress_message.delete()
    except:
        pass

    if not leave:
        return muted_chats
    else:
        for muted_chat in chat_list:
            sleep(0.1)
            try:
                bot.leaveChat(muted_chat, timeout=60)
            except:
                pass
            user_sql.rem_chat(muted_chat)
        return muted_chats

@dev_plus
@run_async
def dbcleanxyz(bot: Bot, update: Update):
    buttons = [[InlineKeyboardButton("Invalid Chats", callback_data="dbclean_invalidchats")]]
    buttons+= [[InlineKeyboardButton("Muted Chats", callback_data="dbclean_mutedchats")]]
    buttons+= [[InlineKeyboardButton("Gbanned Users", callback_data="dbclean_gbans")]]
    update.effective_message.reply_text("What do you want to clean?",
                                    reply_markup=InlineKeyboardMarkup(buttons))

@run_async
def dbclean_callback(bot: Bot, update: Update):
    msg = update.effective_message
    query = update.callback_query
    if query.from_user.id in DEV_USERS:
        pass
        if query.data == 'dbclean_invalidchats':
            msg.edit_text("Getting Invalid Chat Count ...")
            invalid_chat_count = get_invalid_chats(bot, update)
            reply = f"Total invalid chats - {invalid_chat_count}"

            if invalid_chat_count > 0:
                buttons = [
                    [InlineKeyboardButton("Remove Invalid Chats", callback_data=f"db_clean_inavlid_chats")]
                ]

                update.effective_message.reply_text(reply, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                reply_clear = "No Invalid Chats."
                update.effective_message.reply_text(reply_clear)


        #Muted Chats
        if query.data == 'dbclean_mutedchats':
            msg.edit_text("Getting Muted Chat Count ...")
            muted_chat_count = get_muted_chats(bot, update)
            reply = f"Muted Chats - {muted_chat_count}"

            if muted_chat_count > 0:
                buttons = [
                    [InlineKeyboardButton("Leave Muted Chats", callback_data=f"db_clean_muted_chats")]
                ]

                update.effective_message.reply_text(reply, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                reply_clear = "I'm not muted in any Chats."
                update.effective_message.reply_text(reply_clear)

        #Invalid Gbans
        if query.data == 'dbclean_gbans':
            msg.edit_text("Getting Invalid Gban Count ...")
            invalid_gban_count = get_invalid_gban(bot, update)
            reply = f"Invalid Gbans - {invalid_gban_count}"

            if invalid_gban_count > 0:
                buttons = [
                    [InlineKeyboardButton("Remove Invalid Gbans", callback_data=f"db_clean_invalid_gbans")]
                ]

                update.effective_message.reply_text(reply, reply_markup=InlineKeyboardMarkup(buttons))
            else:
                reply_clear = "No Invalid Gbans"
                update.effective_message.reply_text(reply_clear)

    else:
        query.answer("You are not allowed to use this command.")

@run_async
def callback_button(bot: Bot, update: Update):
    query = update.callback_query
    message = query.message
    chat_id = update.effective_chat.id
    query_type = query.data

    admin_list = [OWNER_ID] + DEV_USERS
    bot.answer_callback_query(query.id)

    if query_type == "db_clean_muted_chats":
        if query.from_user.id in admin_list:
            bot.editMessageText("Leaving chats ...", chat_id, message.message_id)
            chat_count = get_muted_chats(bot, update, True)
            bot.sendMessage(chat_id, f"Left {chat_count} chats.")
        else:
            query.answer("You are not allowed to use this.")

    elif query_type == "db_clean_inavlid_chats":
        if query.from_user.id in admin_list:
            bot.editMessageText("Cleaning up DB ...", chat_id, message.message_id)
            invalid_chat_count = get_invalid_chats(bot, update, True)
            reply = "Cleaned up {} chats from DB. ".format(invalid_chat_count)
            bot.sendMessage(chat_id, reply)
        else:
            query.answer("You are not allowed to use this.")

    elif query_type == "db_clean_invalid_gbans":
        if query.from_user.id in admin_list:
            bot.editMessageText("Removing Invalid Gbans from DB ...", chat_id, message.message_id)
            invalid_gban_count = get_invalid_gban(bot, update, True)
            reply = "Cleaned up {} gbanned users from DB.".format(invalid_gban_count)
            bot.sendMessage(chat_id, reply)
        else:
            query.answer("You are not allowed to use this.")

DBCLEAN_HANDLER = CommandHandler("dbclean", dbcleanxyz)
DBCLEAN_CALLBACKHANDLER = CallbackQueryHandler(dbclean_callback, pattern='dbclean_.*')
CLEANER_HANDLER = CallbackQueryHandler(callback_button, pattern='db_.*')

dispatcher.add_handler(DBCLEAN_HANDLER)
dispatcher.add_handler(DBCLEAN_CALLBACKHANDLER)
dispatcher.add_handler(CLEANER_HANDLER)

__mod_name__ = "DB Clean"
__handlers__ = [DBCLEAN_HANDLER, DBCLEAN_CALLBACKHANDLER, CLEANER_HANDLER]
