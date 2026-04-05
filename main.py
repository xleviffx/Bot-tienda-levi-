import os, sqlite3, logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURACIÓN ---
ADMIN_ID = 8426713423 
MI_CONTACTO = "https://t.me/xleviffx"

# --- BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    cursor.execute('CREATE TABLE IF NOT EXISTS usuarios (id INTEGER PRIMARY KEY, saldo REAL, autorizado INTEGER)')
    cursor.execute('CREATE TABLE IF NOT EXISTS inventario (id INTEGER PRIMARY KEY, producto TEXT, precio_id TEXT, key TEXT)')
    cursor.execute('CREATE TABLE IF NOT EXISTS historial (id INTEGER PRIMARY KEY AUTO_INCREMENT, user_id INTEGER, detalle TEXT)')
    conn.commit()
    conn.close()

init_db()

# --- FUNCIONES DE APOYO ---
def db_query(query, params=(), fetch=False):
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    res = cursor.fetchall() if fetch else None
    conn.commit()
    conn.close()
    return res

# --- COMANDOS ADMIN ---
async def dar_acceso(update, context):
    if update.effective_user.id != ADMIN_ID: return
    try:
        target_id = int(context.args[0])
        db_query("INSERT OR REPLACE INTO usuarios (id, saldo, autorizado) VALUES (?, 0, 1)", (target_id,))
        await update.message.reply_text(f"✅ Usuario {target_id} autorizado.")
    except: await update.message.reply_text("Uso: /acceso ID")

async def dar_saldo(update, context):
    if update.effective_user.id != ADMIN_ID: return
    try:
        tid, monto = int(context.args[0]), float(context.args[1])
        db_query("UPDATE usuarios SET saldo = saldo + ? WHERE id = ?", (monto, tid))
        await update.message.reply_text(f"💰 Saldo actualizado para {tid}")
    except: await update.message.reply_text("Uso: /dar ID MONTO")

async def add_key(update, context):
    if update.effective_user.id != ADMIN_ID: return
    try:
        prod, precio_id, key = context.args[0], context.args[1], context.args[2]
        db_query("INSERT INTO inventario (producto, precio_id, key) VALUES (?, ?, ?)", (prod, precio_id, key))
        await update.message.reply_text(f"🔑 Key añadida a {prod} ({precio_id})")
    except: await update.message.reply_text("Uso: /addkey [ios/android/cert] [precio_id] [key]\nEjemplo: /addkey ios 31d ABCD-123")

# --- MENÚS ---
async def start(update, context):
    uid = update.effective_user.id
    user_data = db_query("SELECT autorizado, saldo FROM usuarios WHERE id = ?", (uid,), True)
    
    if uid != ADMIN_ID and (not user_data or user_data[0][0] == 0):
        kb = [[InlineKeyboardButton("📩 Contactar para Acceso", url=MI_CONTACTO)]]
        await update.message.reply_text(f"❌ **ACCESO DENEGADO**\nID: `{uid}`", reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')
        return

    txt = "👋 ¡Bienvenido Jefe!" if uid == ADMIN_ID else "🛒 Bienvenido a la Tienda"
    kb = [
        [InlineKeyboardButton("👤 Perfil", callback_data='p'), InlineKeyboardButton("🛒 Productos", callback_data='cat')],
        [InlineKeyboardButton("🔑 Últimas 10 Keys", callback_data='h')]
    ]
    await update.message.reply_text(txt, reply_markup=InlineKeyboardMarkup(kb))

async def callback_handler(update, context):
    q = update.callback_query
    await q.answer()
    uid = q.from_user.id

    if q.data == 'p':
        res = db_query("SELECT saldo FROM usuarios WHERE id = ?", (uid,), True)
        saldo = res[0][0] if res else 0.0
        txt = f"👤 **PERFIL**\nID: `{uid}`\nNombre: {q.from_user.first_name}\n💰 Balance: ${saldo}"
        kb = [[InlineKeyboardButton("⬅️ ATRÁS", callback_data='inicio')]]
        await q.edit_message_text(txt, reply_markup=InlineKeyboardMarkup(kb), parse_mode='Markdown')

    elif q.data == 'cat':
        kb = [
            [InlineKeyboardButton("🍎 IOS", callback_data='ios'), InlineKeyboardButton("🤖 ANDROID", callback_data='and')],
            [InlineKeyboardButton("📜 CERTIFICADO APPLE", callback_data='cert')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='inicio')]
        ]
        await q.edit_message_text("Selecciona Categoría:", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data == 'ios':
        kb = [[InlineKeyboardButton("💎 FLOURITE", callback_data='flour')], [InlineKeyboardButton("⬅️ ATRÁS", callback_data='cat')]]
        await q.edit_message_text("Productos iOS:", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data == 'flour':
        kb = [
            [InlineKeyboardButton("🗓️ 31 DÍAS - $18", callback_data='buy_ios_31d_18')],
            [InlineKeyboardButton("🗓️ 7 DÍAS - $9", callback_data='buy_ios_7d_9')],
            [InlineKeyboardButton("🗓️ 1 DÍA - $3", callback_data='buy_ios_1d_3')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='ios')]
        ]
        await q.edit_message_text("Opciones Flourite:", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data == 'inicio':
        kb = [[InlineKeyboardButton("👤 Perfil", callback_data='p'), InlineKeyboardButton("🛒 Productos", callback_data='cat')]]
        await q.edit_message_text("Menú Principal:", reply_markup=InlineKeyboardMarkup(kb))

if __name__ == '__main__':
    t = os.environ.get("BOT_TOKEN")
    app = ApplicationBuilder().token(t).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("acceso", dar_acceso))
    app.add_handler(CommandHandler("dar", dar_saldo))
    app.add_handler(CommandHandler("addkey", add_key))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.run_polling(drop_pending_updates=True)
