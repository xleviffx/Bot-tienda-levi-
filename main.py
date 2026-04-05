import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURACIÓN ---
ADMIN_ID = 123456789 # <--- ¡PON TU ID AQUÍ!
MI_CONTACTO = "https://t.me"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    # SISTEMA DE ACCESO DENEGADO
    if user.id != ADMIN_ID: 8426713423
        keyboard = [[InlineKeyboardButton("📩 Contactar Admin", url=MI_CONTACTO)]]
        await update.message.reply_text(
            f"❌ **ACCESO DENEGADO**\n\nTu ID: `{user.id}`\nEnvía este ID al dueño para acceso.",
            parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(keyboard))
        return

    # MENÚ PRINCIPAL PARA TI (EL JEFE)
    keyboard = [
        [InlineKeyboardButton("👤 Perfil", callback_data='perfil')],
        [InlineKeyboardButton("🛒 Productos", callback_data='productos')],
        [InlineKeyboardButton("🔑 Últimas 10 Keys", callback_data='keys')]
    ]
    await update.message.reply_text(f"👋 ¡Bienvenido Jefe! ¿Qué haremos hoy?", 
                                   reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == 'productos':
        keyboard = [
            [InlineKeyboardButton("🍎 IOS", callback_data='cat_ios')],
            [InlineKeyboardButton("🤖 ANDROID", callback_data='cat_android')],
            [InlineKeyboardButton("💻 PC", callback_data='cat_pc')],
            [InlineKeyboardButton("📜 CERTIFICADO APPLE", callback_data='cat_cert')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='main_menu')]
        ]
        await query.edit_message_text("Selecciona una categoría:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'cat_ios':
        keyboard = [
            [InlineKeyboardButton("💎 FLOURITE", callback_data='prod_flourite')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='productos')]
        ]
        await query.edit_message_text("Sección IOS:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'prod_flourite':
        keyboard = [
            [InlineKeyboardButton("🗓️ 31 DÍAS - 18$", callback_data='buy')],
            [InlineKeyboardButton("🗓️ 7 DÍAS - 9$", callback_data='buy')],
            [InlineKeyboardButton("🗓️ 1 DÍA - 3$", callback_data='buy')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='cat_ios')]
        ]
        await query.edit_message_text("Precios FLOURITE:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'cat_cert':
        keyboard = [
            [InlineKeyboardButton("📜 UN AÑO - 5$", callback_data='buy')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='productos')]
        ]
        await query.edit_message_text("CERTIFICADO APPLE (2 Meses Garantía):", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data == 'main_menu':
        # Volver al inicio llamando a la función start manualmente
        await query.edit_message_text("Volviendo al menú...")
        # (Aquí podrías repetir el teclado del start)

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_buttons))
    app.run_polling()
