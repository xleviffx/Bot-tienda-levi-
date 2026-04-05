import os
import sqlite3
import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, CallbackQueryHandler

# --- CONFIGURACIÓN ---
ADMIN_ID = 8426713423 
MI_CONTACTO = "https://t.me"

# --- BASE DE DATOS ---
def init_db():
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS usuarios 
                      (id INTEGER PRIMARY KEY, saldo REAL DEFAULT 0, autorizado INTEGER DEFAULT 0)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS inventario 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, producto TEXT, duracion TEXT, precio REAL, key TEXT)''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS historial 
                      (id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, detalle TEXT)''')
    conn.commit()
    conn.close()

init_db()

def db_query(query, params=(), fetch_one=False, fetch_all=False):
    conn = sqlite3.connect('tienda.db')
    cursor = conn.cursor()
    cursor.execute(query, params)
    res = None
    if fetch_one: res = cursor.fetchone()
    if fetch_all: res = cursor.fetchall()
    conn.commit()
    conn.close()
    return res

# --- MENÚS ---
def main_kb(uid):
    btns = [
        [InlineKeyboardButton("👤 Perfil", callback_data='perfil'), InlineKeyboardButton("🛒 Productos", callback_data='cat')],
        [InlineKeyboardButton("🔑 Últimas 10 Keys", callback_data='historial')]
    ]
    return InlineKeyboardMarkup(btns)

# --- COMANDOS ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    user = db_query("SELECT autorizado FROM usuarios WHERE id = ?", (uid,), fetch_one=True)
    
    if uid != ADMIN_ID and (not user or user[0] == 0):
        kb = InlineKeyboardMarkup([[InlineKeyboardButton("📩 Contactar Admin", url=MI_CONTACTO)]])
        await update.message.reply_text(f"❌ **ACCESO DENEGADO**\nTu ID: `{uid}`", reply_markup=kb, parse_mode='Markdown')
        return

    txt = "👋 ¡Bienvenido Jefe!" if uid == ADMIN_ID else "🛒 Menú de Ventas"
    await update.message.reply_text(txt, reply_markup=main_kb(uid))

# Comandos Admin
async def dar_saldo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        uid, monto = int(context.args[0]), float(context.args[1])
        db_query("INSERT OR IGNORE INTO usuarios (id, autorizado) VALUES (?, 1)", (uid,))
        db_query("UPDATE usuarios SET saldo = saldo + ?, autorizado = 1 WHERE id = ?", (monto, uid))
        await update.message.reply_text(f"💰 Saldo de ${monto} añadido a {uid}")
    except: await update.message.reply_text("Uso: /dar ID MONTO")

async def add_key(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != ADMIN_ID: return
    try:
        p, d, pr, k = context.args[0], context.args[1], float(context.args[2]), context.args[3]
        db_query("INSERT INTO inventario (producto, duracion, precio, key) VALUES (?, ?, ?, ?)", (p, d, pr, k))
        await update.message.reply_text(f"✅ Key guardada en {p} {d}")
    except: await update.message.reply_text("Uso: /addkey [ios/and/cert] [1d/7d/31d] [precio] [key]")

# --- MANEJADOR DE BOTONES ---
async def query_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    uid = query.from_user.id

    if query.data == 'perfil':
        u = db_query("SELECT saldo FROM usuarios WHERE id = ?", (uid,), fetch_one=True)
        s = u[0] if u else 0.0
        txt = f"👤 **PERFIL**\nID: `{uid}`\nNombre: {query.from_user.first_name}\n💰 Balance: ${s}"
        await query.edit_message_text(txt, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ ATRÁS", callback_data='inicio')]]), parse_mode='Markdown')

    elif query.data == 'cat':
        btns = [
            [InlineKeyboardButton("🍎 IOS", callback_data='ios'), InlineKeyboardButton("🤖 ANDROID", callback_data='and')],
            [InlineKeyboardButton("📜 CERTIFICADO APPLE", callback_data='cert')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='inicio')]
        ]
        await query.edit_message_text("Selecciona Categoría:", reply_markup=InlineKeyboardMarkup(btns))

    elif query.data == 'ios':
        btns = [[InlineKeyboardButton("💎 FLOURITE", callback_data='flour')], [InlineKeyboardButton("⬅️ ATRÁS", callback_data='cat')]]
        await query.edit_message_text("Productos iOS:", reply_markup=InlineKeyboardMarkup(btns))

    elif query.data == 'flour':
        btns = [
            [InlineKeyboardButton("🗓️ 31 DÍAS - $18", callback_data='buy_ios_31d_18')],
            [InlineKeyboardButton("🗓️ 7 DÍAS - $9", callback_data='buy_ios_7d_9')],
            [InlineKeyboardButton("🗓️ 1 DÍA - $3", callback_data='buy_ios_1d_3')],
            [InlineKeyboardButton("⬅️ ATRÁS", callback_data='ios')]
        ]
        await query.edit_message_text("Precios Flourite:", reply_markup=InlineKeyboardMarkup(btns))

    elif query.data == 'inicio':
        await query.edit_message_text("Menú Principal:", reply_markup=main_kb(uid))

if __name__ == '__main__':
    # LEER TOKEN DE RAILWAY (Asegúrate que en Railway se llame BOT_TOKEN)
    token_env = os.environ.get("BOT_TOKEN")
    
    if not token_env:
        print("❌ ERROR: No se encontró la variable BOT_TOKEN en Railway.")
    else:
        app = ApplicationBuilder().token(token_env).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("dar", dar_saldo))
        app.add_handler(CommandHandler("addkey", add_key))
        app.add_handler(CallbackQueryHandler(query_handler))
        print("✅ Bot iniciado correctamente")
        app.run_polling(drop_pending_updates=True)
