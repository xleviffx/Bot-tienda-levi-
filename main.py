import telebot
from telebot import types
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- 1. CONFIGURACIÓN DEL JEFE ---
ADMIN_ID = 8426713423
MI_USER = "xleviffx"

# --- 2. EL STOCK (Pon tus códigos aquí) ---
stock_ios_31 = ["KEY-IOS-31-01"]
stock_ios_7 = ["KEY-IOS-7-01"]
stock_ios_1 = ["KEY-IOS-1-01"]
stock_android_31 = ["KEY-DRIP-31-01"]
stock_certificados = ["CERT-01"]

# Bases de datos temporales
usuarios_autorizados = []
saldos = {}
historial_keys = {}

PRECIOS = {"f31": 18, "f7": 9, "f1": 3, "d31": 11, "cert": 5}

def menu_principal():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 Mi Perfil", "🛒 Productos")
    markup.add("🔑 Últimas Keys")
    return markup

@bot.message_handler(func=lambda m: m.from_user.id not in usuarios_autorizados and m.from_user.id != ADMIN_ID)
def restringido(m):
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("📩 Contactar Jefe", url=f"https://t.me{MI_USER}"))
    bot.send_message(m.chat.id, f"🚫 **ACCESO RESTRINGIDO**\nTu ID: `{m.from_user.id}`", reply_markup=kb, parse_mode="Markdown")

@bot.message_handler(commands=['start'])
def inicio(m):
    uid = m.from_user.id
    if uid not in saldos:
        saldos[uid] = 0.0
        historial_keys[uid] = []
    if uid == ADMIN_ID:
        bot.send_message(m.chat.id, "👑 **BIENVENIDO JEFE**\nPlan Hobby Activo 24/7.", parse_mode="Markdown")
    bot.send_message(m.chat.id, "✅ Sistema de Ventas Activo.", reply_markup=menu_principal())

@bot.message_handler(func=lambda m: m.text in ["👤 Mi Perfil", "🛒 Productos", "🔑 Últimas Keys"])
def botones(m):
    uid = m.from_user.id
    if m.text == "👤 Mi Perfil":
        bot.send_message(m.chat.id, f"📌 **PERFIL**\n👤 Usuario: @{m.from_user.username}\n🆔 ID: `{uid}`\n💰 Saldo: ${saldos.get(uid, 0.0)}")
    elif m.text == "🛒 Productos":
        kb = types.InlineKeyboardMarkup()
        kb.add(types.InlineKeyboardButton("🍎 IOS", callback_data="cat_ios"), types.InlineKeyboardButton("🤖 ANDROID", callback_data="cat_and"))
        kb.add(types.InlineKeyboardButton("📜 CERTIFICADO", callback_data="cat_cert"))
        bot.send_message(m.chat.id, "Selecciona categoría:", reply_markup=kb)
    elif m.text == "🔑 Últimas Keys":
        keys = historial_keys.get(uid, [])
        msg = "\n".join([f"• `{k}`" for k in keys[-5:]]) if keys else "Sin compras."
        bot.send_message(m.chat.id, f"🎟 **TUS ÚLTIMAS 5 KEYS:**\n\n{msg}", parse_mode="Markdown")

@bot.callback_query_handler(func=lambda call: True)
def compras(call):
    uid = call.from_user.id
    m = types.InlineKeyboardMarkup()
    if call.data == "cat_ios":
        m.add(types.InlineKeyboardButton("💎 FLOURITE", callback_data="sub_f"))
        bot.edit_message_text("🍎 **PRODUCTOS IOS:**", call.message.chat.id, call.message.message_id, reply_markup=m)
    elif call.data == "sub_f":
        m.add(types.InlineKeyboardButton(f"31 Días - ${PRECIOS['f31']}", callback_data="buy_f31"))
        m.add(types.InlineKeyboardButton(f"7 Días - ${PRECIOS['f7']}", callback_data="buy_f7"))
        m.add(types.InlineKeyboardButton(f"1 Día - ${PRECIOS['f1']}", callback_data="buy_f1"))
        bot.edit_message_text("💎 **FLOURITE:**", call.message.chat.id, call.message.message_id, reply_markup=m)
    elif call.data.startswith("buy_"):
        pk = call.data.replace("buy_", "")
        pr = PRECIOS.get(pk, 999)
        stk = {"f31": stock_ios_31, "f7": stock_ios_7, "f1": stock_ios_1, "d31": stock_android_31, "cert": stock_certificados}
        lista = stk.get(pk)
        if saldos.get(uid, 0.0) >= pr:
            if lista:
                key = lista.pop(0)
                saldos[uid] -= pr
                historial_keys[uid].append(key)
                bot.send_message(call.message.chat.id, f"✅ **COMPRA EXITOSA**\n\n🎟 Key: `{key}`\n💰 Saldo: ${saldos[uid]}", parse_mode="Markdown")
            else: bot.answer_callback_query(call.id, "❌ Sin stock.", show_alert=True)
        else: bot.answer_callback_query(call.id, f"❌ Saldo insuficiente (${pr})", show_alert=True)

@bot.message_handler(commands=['autorizar'])
def auth(m):
    if m.from_user.id == ADMIN_ID:
        try:
            nuevo = int(m.text.split()[1])
            if nuevo not in usuarios_autorizados: usuarios_autorizados.append(nuevo)
            bot.reply_to(m, f"✅ ID {nuevo} autorizado.")
        except: bot.reply_to(m, "Uso: /autorizar ID")

@bot.message_handler(commands=['recargar'])
def rec(m):
    if m.from_user.id == ADMIN_ID:
        try:
            p = m.text.split()
            tid, mon = int(p[1]), float(p[2])
            saldos[tid] = saldos.get(tid, 0.0) + mon
            bot.send_message(m.chat.id, f"✅ ID {tid} recargado con ${mon}.")
            bot.send_message(tid, f"💰 ¡Recarga exitosa! Tienes ${saldos[tid]}")
        except: bot.reply_to(m, "Uso: /recargar ID MONTO")

bot.infinity_polling()
