import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURACIÓN ---
ADMIN_ID = 8426713423  # <--- TU ID YA ESTÁ PUESTO AQUÍ
MI_CONTACTO = "https://t.me"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    
    # SISTEMA DE ACCESO (WHITELIST)
    if user_id != ADMIN_ID:
        kb = [[InlineKeyboardButton("📩 Contactar Admin", url=MI_CONTACTO)]]
        await update.message.reply_text(
            f"❌ **ACCESO DENEGADO**\n\nTu ID es: `{user_id}`\nEnvía este ID al administrador para que te autorice.",
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(kb)
        )
        return

    # MENÚ PARA EL JEFE (TÚ)
    kb = [
        [InlineKeyboardButton("👤 Perfil", callback_data='perfil')],
        [InlineKeyboardButton("🛒 Productos", callback_data='productos')],
        [InlineKeyboardButton("🔑 Últimas 10 Keys", callback_data='keys')]
    ]
    await update.message.reply_text("👋 ¡Bienvenido Jefe! El sistema está listo.", reply_markup=InlineKeyboardMarkup(kb))

async def menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'productos':
        kb = [
            [InlineKeyboardButton("🍎 IOS", callback_data='cat_ios')],
            [InlineKeyboardButton("🤖 ANDROID", callback_data='cat_android')],
            [InlineKeyboardButton("💻 PC", callback_data='cat_pc')],
            [InlineKeyboardButton("📜 CERTIFICADO APPLE", callback_data='cat_cert')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='inicio')]
        ]
        await query.edit_message_text("Selecciona una categoría:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == 'inicio':
        kb = [
            [InlineKeyboardButton("👤 Perfil", callback_data='perfil')],
            [InlineKeyboardButton("🛒 Productos", callback_data='productos')],
            [InlineKeyboardButton("🔑 Últimas 10 Keys", callback_data='keys')]
        ]
        await query.edit_message_text("Menú Principal:", reply_markup=InlineKeyboardMarkup(kb))

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    if token:
        app = ApplicationBuilder().token(token).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(menu_handler))
        print("Bot iniciado con éxito para el Jefe...")
        app.run_polling()
