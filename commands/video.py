from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes

import util
import webbrowser
from util.Lang import Translate


async def links(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user.username

    if await util.Whitelist.NotAllowed(sender):
        await update.message.reply_text(await Translate(update, context, sender, "Commands.whitelist.userNotAllowed"))
        return False

    if not context.args:
        keyboard = [
            [
                InlineKeyboardButton("Hittite Man 🗿", callback_data=1),  # https://youtu.be/x2xr84DhBBM?si=gyZw4UbkrX0XuIfM
                InlineKeyboardButton("Lebron James 🏀", callback_data=2),  # https://vm.tiktok.com/ZGefR4UBd/
            ],
            [
                InlineKeyboardButton("Ronaldo 1 ⚽", callback_data=3),  # https://vm.tiktok.com/ZGefRvajR/
                InlineKeyboardButton("Ronaldo 2 ⚽", callback_data=4),  # https://vm.tiktok.com/ZGefRqtUh/
            ]
        ]

        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(await Translate(update, context, update.effective_user.username, "Commands.Video.chooseVideo"), reply_markup=reply_markup)
        context.user_data["urlImported"] = None

    elif len(context.args) == 1:
        urlImported = context.args[0]
        webbrowser.open(urlImported)
        videoName = " prova "
        await update.message.reply_text(await Translate(update, context, sender, "Commands.Video.selected"))
    elif len(context.args) > 1:
        await update.message.reply_text(await Translate(update, context, sender, "Commands.Video.errorUrl"))


async def linksButtons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    sender = update.effective_user.username
    query = update.callback_query
    await query.answer()

    if query.data == "1":
        urlSelected = "https://youtu.be/x2xr84DhBBM?si=gyZw4UbkrX0XuIfM"
        videoName = "Hittite Man 🗿"
    elif query.data == "2":
        urlSelected = "https://www.youtube.com/shorts/5y_cl3WIO6A"
        videoName = "Lebron James 🏀"
    elif query.data == "3":
        urlSelected = "https://www.youtube.com/watch?v=ajJNI2Yz3UY"
        videoName = "Ronaldo ⚽"
    elif query.data == "4":
        urlSelected = "https://www.youtube.com/watch?v=xvFZjo5PgG0"
        videoName = "RickRoll "
    else:
        await query.edit_message_text(text=f"{await Translate(update, context, sender, "Commands.Video.errorQuery")}")
        return False

    webbrowser.open(urlSelected)
    await query.edit_message_text(text=f"{await Translate(update, context, sender, "Commands.Video.selected")} {videoName}")
