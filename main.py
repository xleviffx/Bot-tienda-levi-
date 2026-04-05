import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURACIÓN ---
ADMIN_ID = 8426713423 
MI_CONTACTO = "https://t.me"

# --- TECLADOS ---
def main_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("👤 Perfil", callback_data='perfil')],
        [InlineKeyboardButton("🛒 Productos", callback_data='productos')],
        [InlineKeyboardButton("🔑 Últimas 10 Keys", callback_data='keys')]
    ])

def productos_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍎 IOS", callback_data='cat_ios')],
        [InlineKeyboardButton("🤖 ANDROID", callback_data='cat_android')],
        [InlineKeyboardButton("📜 CERTIFICADO APPLE", callback_data='cat_cert')],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data='inicio')]
    ])

def ios_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("💎 FLOURITE", callback_data='prod_flourite')],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data='productos')]
    ])

def flourite_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🗓️ 31 DÍAS - 18$", callback_data='buy')],
        [InlineKeyboardButton("🗓️ 7 DÍAS - 9$", callback_data='buy')],
        [InlineKeyboardButton("🗓️ 1 DÍA - 3$", callback_data='buy')],
        [InlineKeyboardButton("⬅️ ATRÁS", callback_data='cat_ios')]
    ])

# --- FUNCIONES ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    if user_id != ADMIN_ID:
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("📩 Contactar Admin", url=MI_CONTACTO)]])
        await update.message.reply_text(f"❌ ACCESO DENEGADO\nID: {user_id}", reply_markup=kb)
        return
    await update.message.reply_text("👋 ¡Bienvenido Jefe!", reply_markup=main_menu_kb())

async def query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'productos':
        await query.edit_message_text("Selecciona una categoría:", reply_markup=productos_kb())
    elif query.data == 'cat_ios':
        await query.edit_message_text("Sección IOS:", reply_markup=ios_kb())
    elif query.data == 'prod_flourite':
        await query.edit_message_text("Precios FLOURITE:", reply_markup=flourite_kb())
    elif query.data == 'cat_cert':
        txt = "📜 CERTIFICADO APPLE (1 AÑO - 5$)\n(2 Meses Garantía)"
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ATRÁS", callback_data='productos')]])
        await query.edit_message_text(txt, reply_markup=kb)
    elif query.data == 'inicio':
        await query.edit_message_text("Menú Principal:", reply_markup=main_menu_kb())

if __name__ == '__main__':
    token = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(query_handler))
    app.run_polling()
