import platform
import subprocess

from telegram import Update
from telegram.ext import ContextTypes


async def check_version(update: Update, context: ContextTypes.DEFAULT_TYPE):
    try:
        result = subprocess.run(['python', '--version'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        ver = result.stdout.decode('utf-8').strip()
        await update.message.reply_text(f"Python è installato! Versione: {ver}")

    except FileNotFoundError:
        await update.message.reply_text("Python non è installato. Sto procedendo con l'installazione...")
        if platform.system() == "Linux":
            try:
                subprocess.check_call(['sudo', 'apt-get', 'update'])
                subprocess.check_call(['sudo', 'apt-get', 'install', '-y', 'python3'])
                await update.message.reply_text("Python è stato installato con successo.")
            except subprocess.CalledProcessError:
                await update.message.reply_text("Errore durante l'installazione di Python.")
        elif platform.system() == "Windows":
            try:
                subprocess.check_call(['python-3.12.2.exe'])
                await update.message.reply_text("Python è stato installato con successo.")
            except subprocess.CalledProcessError:
                await update.message.reply_text("Errore durante l'installazione di Python.")
