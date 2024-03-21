import json

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from util.Lang import Translate


async def NotAllowed(sender):

    with (open("config.json", 'r+') as file):
        data = json.load(file)
        found = False

    for user in data["users"]:
        if user["username"] == sender or sender == "ali3n07":
            found = True
            break

    if found:
        return False
    else:
        return True


async def Whitelist(update: Update, context: ContextTypes.DEFAULT_TYPE):

    sender = update.effective_user.username

    if await NotAllowed(sender):
        await update.message.reply_text(await Translate(update, context, sender, "Commands.whitelist.userNotAllowed"))
        return False

    with (open("config.json", 'r+') as file):
        data = json.load(file)
        userListStr = ""
        usersAdded = 0

        if len(context.args) >= 1:
            for userCommand in context.args:
                if not any(userConfig["username"] == userCommand for userConfig in data['users']):
                    userListStr += f"{userCommand}, "
                    data['users'].append({
                        "username": userCommand,
                        "lang": "en_GB"
                    })
                    usersAdded += 1

            file.seek(0)
            json.dump(data, file, indent=4)
            file.truncate()

            if usersAdded == 1:
                userListStr = await Translate(update, context, update.effective_user.username, "Commands.whitelist.userAdded") + userListStr
            elif usersAdded > 1:
                userListStr = await Translate(update, context, update.effective_user.username, "Commands.whitelist.usersAdded") + userListStr
            else:
                await update.message.reply_text(await Translate(update, context, update.effective_user.username, "Commands.whitelist.noUserAdded"))


            userListStr = userListStr.rstrip(", ")

            await update.message.reply_text(userListStr)


        else:
            whitelist = await Translate(update, context, sender, "Commands.whitelist.userWhitelisted")
            for user in data["users"]:
                whitelist += ("\n \\- " + user["username"])

            await update.message.reply_text(whitelist, parse_mode=ParseMode.MARKDOWN_V2)

