from telegram.constants import ParseMode
from telegram import Update
from telegram.ext import ContextTypes

from util.lang import Translate
import util.whitelist
import rotatescreen
import time


async def rotate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rotationTimes = 5
    rotationDegrees = 90
    rotationDelay = 1
    screens = rotatescreen.get_displays()
    sender = update.effective_user.username
    start_pos = []

    if not await util.whitelist.allowed(sender):
        await update.message.reply_text(await Translate(update, context, sender, "Commands.whitelist.UserNotAllowed"))
        return False

    for display in screens:
        start_pos.append(display.current_orientation)

    if len(context.args) >= 1:
        if context.args[0].isnumeric():
            if not (int(context.args[0]) > 100 or int(context.args[0]) <= 0):
                rotationTimes = round(float(context.args[0])) + 1
            else:
                await update.message.reply_text(await Translate(update, context, sender, "Commands.rotateScreen.rotationTimesError2"))
                return False
        else:
            await update.message.reply_text(await Translate(update, context, sender, "Commands.rotateScreen.rotationTimesError1"), parse_mode=ParseMode.MARKDOWN_V2)
            return False

    if len(context.args) >= 2:
        if context.args[1].isnumeric():
            if int(context.args[1]) != 0 or int(context.args[1]) != 90 or int(context.args[1]) != 180 or int(context.args[1]) != 270:
                rotationDegrees = round(float(context.args[1]))
            else:
                await update.message.reply_text(await Translate(update, context, sender, "Commands.rotateScreen.rotationDegreesError2"), parse_mode=ParseMode.MARKDOWN_V2)
                return False
        else:
            await update.message.reply_text(await Translate(update, context, sender, "Commands.rotateScreen.rotationDegreesError1"), parse_mode=ParseMode.MARKDOWN_V2)
            return False

    if len(context.args) >= 3:
        try:
            rotationDelay = float(context.args[2])
        except ValueError:
            try:
                rotationDelay = int(context.args[2])
            except ValueError:
                await update.message.reply_text(await Translate(update, context, sender, "Commands.rotateScreen.rotationDelayError1"), parse_mode=ParseMode.MARKDOWN_V2)
                return False

    for i in range(1, rotationTimes):
        j = 0
        for display in screens:
            pos = (start_pos[j] + i * rotationDegrees) % 360
            display.rotate_to(pos)
            j += 1

        time.sleep(rotationDelay)

    await update.message.reply_text(await Translate(update, context, sender, "Commands.rotateScreen.success"))
    return True
