"""
Steps for update the executable:
 - download the newest .exe file
 - stop this .exe file
 - update other files (like config file)
 - execute the newest .exe file
"""
import json
import sys

import requests
from telegram import Update
from telegram.ext import ContextTypes

from util.debug import debugMode
from util.lang import Translate


async def updateCommand(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user.username

    with (open("config.json", 'r') as file):
        data = json.load(file)
        version = data.get("version")
        print(version)

    #! check if is updated
    #? if True return
    #? else continue
    if await debugMode(sender):
        await update.message.reply_text("[DEBUG] " + str(await Translate(update, context, sender, "Commands.update.getDownloadUrl")))
    #* get urls
    #? https://api.github.com/repos/<USER>/<REPO_NAME>/releases/latest
    url = "https://api.github.com/repos/alien0-7/Telegram-bot/releases/latest"
    file_urls = await get_urls(url, "assets_url")
    if await debugMode(sender):
        await update.message.reply_text("[DEBUG] " + str(await Translate(update, context, sender, "Commands.update.downloadFiles"))) #! stamp list of files or file
    #* download
    if file_urls:
        for url in file_urls:
            response = requests.get(url)
            if response.status_code == 200:

                filename = url[url.rfind("/") + 1:]
                with open(filename, 'wb') as file:
                    file.write(response.content)

                print(f"scaricato: {filename}")

            else:
                print("Error2")
    else:
        print("Error1")

    if await debugMode(sender):
        await update.message.reply_text("[DEBUG] " + str(await Translate(update, context, sender, "Commands.update.halfUpdate")))

    sys.exit() # it will self-reopen by the start script



#* Multi file download with assets_url
async def get_urls(url, key):
    response = requests.get(url)
    file_urls = list()
    if response.status_code == 200:
        res = response.json()
        if key == "assets_url":
            assets_url = res[key]
            return await get_urls(assets_url, "browser_download_url")
        else:
            for item in res:
                file_urls.append(item[key])
            return file_urls
    else:
        return