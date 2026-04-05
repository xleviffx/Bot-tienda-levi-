import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURACIÓN ---
ADMIN_ID = 8426713423 
MI_CONTACTO = "https://t.me"

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        kb = [[InlineKeyboardButton("📩 Contactar Admin", url=MI_CONTACTO)]]
        await update.message.reply_text(f"❌ ACCESO DENEGADO\nID: {user_id}", reply_markup=InlineKeyboardMarkup(kb))
        return
    
    kb = [
        [InlineKeyboardButton("👤 Perfil", callback_data='perfil')],
        [InlineKeyboardButton("🛒 Productos", callback_data='productos')],
        [InlineKeyboardButton("🔑 Últimas 10 Keys", callback_data='keys')]
    ]
    await update.message.reply_text("👋 ¡Bienvenido Jefe!", reply_markup=InlineKeyboardMarkup(kb))

async def handle_menus(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'perfil':
        user = query.from_user
        txt = f"👤 **TU PERFIL**\n\nID: `{user.id}`\nNombre: {user.first_name}\nBalance: $0.00 (Próximamente)"
        kb = [[InlineKeyboardButton("⬅️ ATRÁS", callback_data='inicio')]]
        await query.edit_message_text(txt, parse_mode='Markdown', reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == 'productos':
        kb = [
            [InlineKeyboardButton("🍎 IOS", callback_data='ios')],
            [InlineKeyboardButton("🤖 ANDROID", callback_data='android')],
            [InlineKeyboardButton("📜 CERTIFICADO APPLE", callback_data='cert')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='inicio')]
        ]
        await query.edit_message_text("Selecciona una categoría:", reply_markup=InlineKeyboardMarkup(kb))
    
    elif query.data == 'inicio':
        kb = [[InlineKeyboardButton("👤 Perfil", callback_data='perfil')], [InlineKeyboardButton("🛒 Productos", callback_data='productos')]]
        await query.edit_message_text("Menú Principal:", reply_markup=InlineKeyboardMarkup(kb))

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_menus))
    
    # ESTA ES LA LÍNEA QUE DEBES REVISAR:
    app.run_polling(drop_pending_updates=True)
