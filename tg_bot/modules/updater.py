from os import remove
from os import execl
import sys

import git
import asyncio
import random
import re
import time

from collections import deque

import requests

from telegram import Bot, Update, TelegramError
from telegram.ext import CommandHandler, run_async

from tg_bot import HEROKU_API_KEY, HEROKU_APP_NAME, dispatcher
from tg_bot.modules.helper_funcs.chat_status import dev_plus

from contextlib import suppress
import os
import sys
import asyncio

# -- Constants -- #
OFFICIAL_UPSTREAM_REPO = "https://Dc5000:Div2521%23@github.com/Dc5000/HitmanAgent47_Bot"
REPO_REMOTE_NAME = "temponame"
IFFUCI_ACTIVE_BRANCH_NAME = "master"
NO_HEROKU_APP_CFGD = "no heroku application found, but a key given? 😕 "
HEROKU_GIT_REF_SPEC = "HEAD:refs/heads/master"
RESTARTING_APP = "re-starting heroku application"
# -- Constants End -- #


@dev_plus
@run_async
def update(bot: Bot, update: Update):
    try:
        repo = git.Repo()
    except git.exc.InvalidGitRepositoryError as e:
        repo = git.Repo.init()
        origin = repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
        origin.fetch()
        repo.create_head(IFFUCI_ACTIVE_BRANCH_NAME, origin.refs.master)
        repo.heads.master.checkout(True)

    active_branch_name = repo.active_branch.name
    try:
        repo.create_remote(REPO_REMOTE_NAME, OFFICIAL_UPSTREAM_REPO)
    except Exception as e:
        print(e)
        pass

    temp_upstream_remote = repo.remote(REPO_REMOTE_NAME)
    temp_upstream_remote.fetch(active_branch_name)

    temp_upstream_remote.fetch(active_branch_name)
    repo.git.reset("--hard", "FETCH_HEAD")

    if HEROKU_API_KEY is not None:
        import heroku3
        heroku = heroku3.from_key(HEROKU_API_KEY)
        heroku_applications = heroku.apps()
        if len(heroku_applications) >= 1:
            if HEROKU_APP_NAME is not None:
                heroku_app = None
                for i in heroku_applications:
                    if i.name == HEROKU_APP_NAME:
                        heroku_app = i
                if heroku_app is None:
                    update.effective_message.reply_text("Invalid APP Name. Please set the name of your bot in heroku in the var `HEROKU_APP_NAME.`")
                    return
                heroku_git_url = heroku_app.git_url.replace(
                    "https://",
                    "https://api:" + HEROKU_API_KEY + "@"
                )
                if "heroku" in repo.remotes:
                    remote = repo.remote("heroku")
                    remote.set_url(heroku_git_url)
                else:
                    remote = repo.create_remote("heroku", heroku_git_url)

            else:
                update.effective_message.reply_text("Please create the var `HEROKU_APP_NAME` as the key and the name of your bot in heroku as your value.")
                return
        else:
            update.effective_message.reply_text(NO_HEROKU_APP_CFGD)
    else:
        update.effective_message.reply_text("No heroku api key found in `HEROKU_API_KEY` var")

UPDATE_HANDLER = CommandHandler("update", update)

dispatcher.add_handler(UPDATE_HANDLER)

__handlers__ = [UPDATE_HANDLER]
