from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import Update

from util import ConfigJSON, Lang, Whitelist
from commands import rotate


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi 👋, I'm the bot developed by @ali3n07!\nWhat do you want to do today?")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused error {context.error}")


# MAIN
app = Application.builder().token(ConfigJSON.token()).build()

# Command
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("rotate", rotate.rotate))
app.add_handler(CommandHandler("lang", Lang.LangMessage))
app.add_handler(CommandHandler("whitelist", Whitelist.Whitelist))

# Buttons
app.add_handler(CallbackQueryHandler(Lang.LangButtons))

# Error
app.add_error_handler(error)

app.run_polling(poll_interval=3, allowed_updates=Update.ALL_TYPES)
