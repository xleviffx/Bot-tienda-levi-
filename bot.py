import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update: Update, context):
    await update.message.reply_text("¡Listo! El bot está en línea y en inglés.")

if __name__ == '__main__':
    token = os.environ.get("TOKEN")
    if token:
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.run_polling()
