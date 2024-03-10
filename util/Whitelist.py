from telegram.ext import ContextTypes
from telegram import Update
import json

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
                userListStr = await Translate(update, context, update.effective_user.username, "Commands.whitelist.UserAdded") + userListStr
            elif usersAdded > 1:
                userListStr = await Translate(update, context, update.effective_user.username, "Commands.whitelist.UsersAdded") + userListStr
            else:
                await update.message.reply_text(await Translate(update, context, update.effective_user.username, "Commands.whitelist.noUserAdded"))


            userListStr = userListStr.rstrip(", ")

            await update.message.reply_text(userListStr)


        else:
            await update.message.reply_text(await Translate(update, context, update.effective_user.username, "Command.whitelist.noUserSelected"))
