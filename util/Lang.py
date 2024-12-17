from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
import yaml, json, util


async def Translate(update: Update, context: ContextTypes.DEFAULT_TYPE, sender=None, yamlpath=None):
    try:
        with open("config.json", 'r') as jsonfile:
            jsondata = json.load(jsonfile)
            user_lang = "en_GB"
            notFound = True

            for user in jsondata.get("users", []):
                if user["username"] == sender:
                    user_lang = user["lang"]
                    notFound = False
                    break

            if notFound:
                await update.message.reply_text("*You are not authorized to execute this command\\.*", parse_mode=ParseMode.MARKDOWN_V2)
                return

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
        await context.bot.send_message(update.effective_chat.id,"That language file doesn't exist.\nDownloading it...")
        # TODO: Implement download logic


async def LangMessage(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user.username

    if not await util.whitelist.allowed(sender):
        await update.message.reply_text(await Translate(update, context, sender, "Commands.whitelist.userNotAllowed"))
        return False

    keyboard = [
        [
            InlineKeyboardButton("Italiano 🇮🇹", callback_data=str("lang:it_IT")),
            InlineKeyboardButton("English 🇬🇧", callback_data=str("lang:en_GB")),
        ],
        #        [InlineKeyboardButton("Option 3", callback_data="3")],
    ]

    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(await Translate(update, context, update.effective_user.username, "Commands.lang.chooseLang"), reply_markup=reply_markup)


async def LangButtons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    sender = update.effective_user.username

    with (open("config.json", 'r+') as file):
        data = json.load(file)

        if 'users' not in data:
            data['users'] = []

        for user in data['users']:
            if user["username"] == sender:
                user["lang"] = query.data.replace("lang:", "")
                break

        file.seek(0)
        file.truncate()
        json.dump(data, file, indent=4)
    await context.bot.send_message(update.effective_chat.id, await Translate(update, context, sender, "Commands.lang.selected"))
