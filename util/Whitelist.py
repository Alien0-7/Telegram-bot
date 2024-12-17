import json

from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, User
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from util.lang import Translate

async def allowed(sender):
    if sender == "ali3n07":
        return True

    with (open("config.json", 'r') as file):
        data = json.load(file)

    for user in data["users"]:
        if user["username"] == sender:
            return True

    return False


async def whitelist(update: Update, context: ContextTypes.DEFAULT_TYPE):

    sender = update.effective_user.username

    if not await allowed(sender):
        await update.message.reply_text(await Translate(update, context, sender, "Commands.whitelist.userNotAllowed"))
        return False

    with (open("config.json", 'r+') as file):
        data = json.load(file)

        if len(context.args) >= 2:
            if context.args[0] == "add":
                data = await whitelist_adder(update, context, data)
                file.seek(0)
                json.dump(data, file, indent=4)
                file.truncate()

        elif context.args[0] == "rm":
            await whitelist_rm_buttons(update, context, data)

        else:
            whitelist = await Translate(update, context, sender, "Commands.whitelist.userWhitelisted")
            print(data)
            for user in data["users"]:
                whitelist += ("\n \\- " + user["username"])

            await update.message.reply_text(whitelist, parse_mode=ParseMode.MARKDOWN_V2)

async def whitelist_adder(update: Update, context: ContextTypes.DEFAULT_TYPE, data):
    from util.debug import debugMode
    userListStr = ""
    usersAdded = 0
    sender = update.effective_user.username

    if await debugMode(sender):
        for usernameInCommand in context.args[1:]:
            await update.message.reply_text("[DEBUG] " + usernameInCommand)

    for usernameInCommand in context.args[1:]:
        if not any(usernameInCommand == userConfig["username"] for userConfig in data['users']):
            userListStr += f"{usernameInCommand}, "
            data['users'].append({
                "username": usernameInCommand,
                "lang": "en_GB",
                "debugMode": False,
                "is_op": False,
            })
            usersAdded += 1

    if usersAdded == 1:
        userListStr = await Translate(update, context, sender, "Commands.whitelist.userAdded") + userListStr
    elif usersAdded > 1:
        userListStr = await Translate(update, context, sender, "Commands.whitelist.usersAdded") + userListStr
    else:
        await update.message.reply_text(await Translate(update, context, sender, "Commands.whitelist.noUserAdded"))
        return data

    userListStr = userListStr.rstrip(", ")

    await update.message.reply_text(userListStr)
    return data



async def whitelist_rm_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE, data):
    keyboard = []

    for user in data["users"]:
        keyboard.append(InlineKeyboardButton(user["username"], callback_data=f"wl_rm:{user["username"]}"))

    reply_markup = InlineKeyboardMarkup([keyboard[i:i+2] for i in range(0,len(keyboard), 2)]) #sequence of sequence divided by 2
    await update.message.reply_text(await Translate(update, context, update.effective_user.username, "Commands.whitelist.removeFromWhitelist"),reply_markup=reply_markup)

async def whitelist_remover(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    username_to_remove = query.data.replace("wl_rm:", "")

    found = False
    with open("config.json", "r+") as file:
        data = json.load(file)
        for user in data["users"]:
            if username_to_remove == user["username"]:
                found = True
                data["users"].remove(user)
                break
        file.seek(0)
        json.dump(data, file, indent=4)
        file.truncate()

    if found:
        await context.bot.send_message(update.effective_chat.id, await Translate(update, context, update.effective_user.username, "Commands.whitelist.removedSuccessfully"))
    else:
        await context.bot.send_message(update.effective_chat.id, await Translate(update, context, update.effective_user.username, "Commands.whitelist.removedUnsuccessfully"))
