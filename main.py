import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler

async def start(update, context):
    await update.message.reply_text("✅ ¡CONECTADO AL FIN JEFE!")

if __name__ == '__main__':
    # Intentamos leer la variable de Railway
    token_env = os.environ.get("BOT_TOKEN")
    
    # Si Railway no nos da el token, usamos uno de respaldo para probar
    if not token_env:
        print("❌ ERROR: No se encontró la variable BOT_TOKEN en Railway.")
    else:
        print(f"✅ Token detectado correctamente.")
        app = ApplicationBuilder().token(token_env).build()
        app.add_handler(CommandHandler("start", start))
        app.run_polling(drop_pending_updates=True)
