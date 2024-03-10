from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
import yaml
import json


async def Translate(update: Update, context: ContextTypes.DEFAULT_TYPE, sender=None, yamlpath=None):
    try:
        with open("config.json", 'r') as jsonfile:
            jsondata = json.load(jsonfile)
            user_lang = "en_GB"

            for user in jsondata.get("users", []):
                if user["username"] == sender:
                    user_lang = user["lang"]
                    break

            with open(f"lang/{user_lang}.yml", 'r', encoding='utf8') as yamlfile:
                yamldata = yaml.safe_load(yamlfile)

                keys = yamlpath.split('.')
                value = yamldata
                for key in keys:
                    value = value.get(key, None)
                    if value is None:
                        break

                return value


    except FileNotFoundError:
        await context.bot.send_message(chat_id=update.effective_chat.id,
                                       text="The language file doesn't exist.\nDownloading it...")
        # TODO: Implement download logic


async def LangMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Italiano 🇮🇹", callback_data=str("it_IT")),
            InlineKeyboardButton("English 🇬🇧", callback_data=str("en_GB")),
        ],
        #        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(await Translate(update, context, update.effective_user.username, "Commands.Lang.ChooseLang"), reply_markup=reply_markup)


async def LangButtons(update: Update, context: ContextTypes.DEFAULT_TYPE, ):
    query = update.callback_query
    await query.answer()

    sender = update.effective_user.username

    with (open("config.json", 'r+') as file):
        data = json.load(file)

        if 'users' not in data:
            data['users'] = []

        for user in data['users']:
            if user["username"] == sender:
                user["lang"] = query.data
                break

        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)
    await context.bot.send_message(chat_id=update.effective_chat.id, text=await Translate(update, context, sender=sender, yamlpath="Commands.Lang.selected"))
