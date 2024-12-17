import json

from util.lang import Translate
from telegram import Update
from telegram.ext import ContextTypes


async def debug(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from util.whitelist import allowed
    sender = update.effective_user.username

    if not await allowed(sender):
        await update.message.reply_text(await Translate(update, context, sender, "Commands.whitelist.userNotAllowed"))
        return

    if not context.args:
        #*simply toggle it, true => false, false => true
        await toggleDebug(sender, context, update)
        return


    elif len(context.args) == 1:
        #* get value inserted
        #* Ex. /debug true => debugMode: true
        await setDebug(sender, context, update)
        return

    else:
        await update.message.reply_text(await Translate(update, context, sender, "Commands.debug.incorrectUsage"))


async def toggleDebug(sender, context, update):
    try:
        with (open("config.json", 'r+') as file):
            data = json.load(file)

            for user in data['users']:
                if user["username"] == sender:
                    user["debugMode"] = not user.get("debugMode", False)
                    emoji = "✅" if user.get("debugMode", False) else "❌"
                    await context.bot.send_message(update.effective_chat.id, await Translate(update, context, sender,"Commands.debug.selected") + str(user.get("debugMode", False)) + emoji)
                    break

            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=4)

    except Exception as e:
        print(e)

async def setDebug(sender, context, update):
    try:
        boolValue = eval(context.args[0])
        with (open("config.json", 'r+') as file):
            data = json.load(file)

            for user in data['users']:
                if user["username"] == sender:
                    user["debugMode"] = boolValue
                    emoji = "✅" if user.get("debugMode", False) else "❌"
                    await context.bot.send_message(update.effective_chat.id, await Translate(update, context, sender, "Commands.debug.selected") + str(user.get("debugMode", False)) + emoji)
                    break

            file.seek(0)
            file.truncate()
            json.dump(data, file, indent=4)

    except Exception as e:
        print(e)

async def debugMode(sender):
    try:
        with (open("config.json", 'r') as file):
            data = json.load(file)

            for user in data['users']:
                if user["username"] == sender and user.get("debugMode"):
                    return True
        return False
    except Exception as e:
        print(e)