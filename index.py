from telegram.ext import Application, CommandHandler, ContextTypes, CallbackQueryHandler
from telegram import Update, BotCommand

from util import configJSON, lang, whitelist, debug, autoUpdater
from commands import rotate, video, fakeError


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi 👋, I'm the bot developed by @ali3n07!\nWhat do you want to do today?")


async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"update {update} caused error {context.error}")

async def post_init(application: Application):
    commands = [
        BotCommand("rotate", "rotate the screen"),
        BotCommand("video", "display the given link"),
        BotCommand("error", "display a fake error"),
        BotCommand("whitelist", "see who is in the whitelist"),
        BotCommand("lang", "set up language of the bot for you"),
        BotCommand("debug", "see debug messages"),
        BotCommand("update", "update the bot"),
    ]
    await application.bot.set_my_commands(commands)




# MAIN
configJSON.checkConfigJSON() #check and format the JSON config file
app = Application.builder().token(configJSON.token()).post_init(post_init).build()

# Command
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("update", autoUpdater.updateCommand))
app.add_handler(CommandHandler("debug", debug.debug))
app.add_handler(CommandHandler("rotate", rotate.rotate))
app.add_handler(CommandHandler("lang", lang.LangMessage))
app.add_handler(CommandHandler("error", fakeError.winerror))
app.add_handler(CommandHandler("video", video.links))
app.add_handler(CommandHandler("whitelist", whitelist.whitelist))

# Buttons
app.add_handler(CallbackQueryHandler(lang.LangButtons, pattern='^lang:'))
app.add_handler(CallbackQueryHandler(video.linksButtons, pattern='^v_url:'))
app.add_handler(CallbackQueryHandler(whitelist.whitelist_remover, pattern='^wl_rm:'))

# Error
app.add_error_handler(error)

app.run_polling()