import ctypes
import shlex

from telegram.ext import ContextTypes
from telegram import Update

from util.lang import Translate


async def winerror(update: Update, context: ContextTypes.DEFAULT_TYPE):
    MessageBox = ctypes.windll.user32.MessageBoxW
    sender = update.effective_user.username
    message = ""
    title = ""
    typewin = 0

    args = shlex.split(' '.join(context.args))

    if len(args) >= 1:
        message = args[0]

    if len(args) >= 2:
        title = args[1]

    if len(args) >= 3:
        if args[2].lower() == "ok":
            button = 0x0
        elif args[2].lower() == "ok-cancel":
            button = 0x01
        elif args[2].lower() == "yes-no-cancel":
            button = 0x03
        elif args[2].lower() == "yes-no":
            button = 0x04
        else:
            await update.message.reply_text("not good1")#await Translate(update, context, sender,"Commands.error.errorButton")
            return False

        typewin = button

    MessageBox(None, message, title, int(typewin))
    await update.message.reply_text("good")#await Translate(update, context, sender,"Commands.error.success")

"""
    if len(args) >= 4:
        icon = ""

        if args[3] == "exclaim":
            icon = " | 0x30"
        elif args[3] == "info":
            icon = " | 0x40"
        elif args[3] == "stop":
            icon = " | 0x10"
        else:
            await update.message.reply_text("not good2") #await Translate(update, context, sender,"Commands.error.errorIcon")
            return False

        typewin += icon
"""