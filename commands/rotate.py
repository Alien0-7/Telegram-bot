from util.Lang import Translate
import rotatescreen
import time
from telegram import Update
from telegram.ext import ContextTypes, CommandHandler


async def rotate(update: Update, context: ContextTypes.DEFAULT_TYPE):
    rotationTimes = 5
    rotationDegrees = 90
    rotationDelay = 1
    screens = rotatescreen.get_displays()
    sender = update.effective_user.username

    start_pos = []

    for display in screens:
        start_pos.append(display.current_orientation)




    if len(context.args) >= 1:
        if context.args[0].isnumeric():
            if context.args[0] != 0 or context.args[0] != 90 or context.args[0] != 180 or context.args[0] != 270:
                rotationTimes = round(float(context.args[0]))+1
            else:
                await update.message.reply_text(
                    await Translate(update, context, sender, "Commands.rotateScreen.rotationTimesError2"))
        else:
            await update.message.reply_text(
                await Translate(update, context, sender, "Commands.rotateScreen.rotationTimesError1"))

    if len(context.args) >= 2:
        if context.args[1].isnumeric():
            rotationDegrees = round(float(context.args[1]))
        else:
            await update.message.reply_text(
                await Translate(update, context, sender, "Commands.rotateScreen.rotationDegreesError1"))

    if len(context.args) >= 3:
        try:
            rotationDelay = float(context.args[2])
        except ValueError:
            try:
                rotationDelay = int(context.args[2])
            except ValueError:
                await update.message.reply_text(
                    await Translate(update, context, sender, "Commands.rotateScreen.rotationDelayError1"))





    for i in range(1, rotationTimes):
        j = 0
        for display in screens:
            pos = (start_pos[j] + i * rotationDegrees) % 360
            display.rotate_to(pos)
            j += 1

        time.sleep(rotationDelay)

    await update.message.reply_text(await Translate(update, context, sender, "Commands.rotateScreen.success"))
