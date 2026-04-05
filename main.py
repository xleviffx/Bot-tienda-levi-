import telebot
from telebot import types
import os

# --- 1. CONFIGURACIÓN ---
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

ADMIN_ID = 8426713423  # TU ID CONFIGURADO
MI_USER = "xleviffx"   # TU USUARIO DE TELEGRAM

# BASES DE DATOS TEMPORALES
usuarios_autorizados = []
saldos = {}
historial_keys = {}

# PRECIOS DE PRODUCTOS
PRECIOS = {
    "f31": 18, "f7": 9, "f1": 3,
    "d31": 11, "cert": 5
}

# --- 2. MENÚS PRINCIPALES ---
def menu_principal():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 Mi Perfil", "🛒 Productos")
    markup.add("🔑 Últimas Keys")
    return markup

# --- 3. FILTRO DE SEGURIDAD (ACCESO RESTRINGIDO) ---
@bot.message_handler(func=lambda m: m.from_user.id not in usuarios_autorizados and m.from_user.id != ADMIN_ID)
def acceso_denegado(m):
    markup = types.InlineKeyboardMarkup()
    markup.add(types.InlineKeyboardButton("📩 Contactar Jefe", url=f"https://t.me{MI_USER}"))
    bot.send_message(
        m.chat.id, 
        f"🚫 **ACCESO RESTRINGIDO**\n\nTu ID: `{m.from_user.id}`\n\nEnvía tu ID al jefe para que te dé acceso al bot.", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

# --- 4. COMANDO START ---
@bot.message_handler(commands=['start'])
def inicio(m):
    uid = m.from_user.id
    if uid not in saldos:
        saldos[uid] = 0.0
        historial_keys[uid] = []

    if uid == ADMIN_ID:
        bot.send_message(m.chat.id, "👑 **¡BIENVENIDO JEFE!**\nAcceso total activado.", parse_mode="Markdown")
    
    bot.send_message(m.chat.id, "✅ Bienvenido al Sistema de Ventas.", reply_markup=menu_principal())

# --- 5. LÓGICA DE BOTONES DE TEXTO ---
@bot.message_handler(func=lambda m: True)
def manejar_botones(m):
    uid = m.from_user.id
    
    if m.text == "👤 Mi Perfil":
        user = m.from_user.username if m.from_user.username else "Sin User"
        saldo = saldos.get(uid, 0.0)
        bot.send_message(m.chat.id, f"📌 **DATOS DEL PERFIL**\n\n👤 Usuario: @{user}\n🆔 ID: `{uid}`\n💰 Saldo: ${saldo}", parse_mode="Markdown")

    elif m.text == "🛒 Productos":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🍎 IOS", callback_data="cat_ios"), types.InlineKeyboardButton("🤖 ANDROID", callback_data="cat_android"))
        markup.add(types.InlineKeyboardButton("💻 PC", callback_data="cat_pc"), types.InlineKeyboardButton("📜 CERTIFICADO", callback_data="cat_cert"))
        bot.send_message(m.chat.id, "🛒 **CATEGORÍAS:**", reply_markup=markup)

    elif m.text == "🔑 Últimas Keys":
        keys = historial_keys.get(uid, [])
        lista = "\n".join([f"• `{k}`" for k in keys[-5:]]) if keys else "Aún no tienes compras."
        bot.send_message(m.chat.id, f"🎟 **TUS ÚLTIMAS 5 KEYS:**\n\n{lista}", parse_mode="Markdown")

# --- 6. NAVEGACIÓN Y SUBMENÚS ---
@bot.callback_query_handler(func=lambda call: True)
def navegacion(call):
    m = types.InlineKeyboardMarkup()
    
    if call.data == "cat_ios":
        m.add(types.InlineKeyboardButton("💎 FLOURITE", callback_data="sub_flourite"))
        bot.edit_message_text("🍎 **OPCIONES IOS:**", call.message.chat.id, call.message.message_id, reply_markup=m)
    
    elif call.data == "sub_flourite":
        m.add(types.InlineKeyboardButton(f"31 Días - ${PRECIOS['f31']}", callback_data="buy_f31"))
        m.add(types.InlineKeyboardButton(f"7 Días - ${PRECIOS['f7']}", callback_data="buy_f7"))
        m.add(types.InlineKeyboardButton(f"1 Día - ${PRECIOS['f1']}", callback_data="buy_f1"))
        bot.edit_message_text("💎 **FLOURITE (IOS):**", call.message.chat.id, call.message.message_id, reply_markup=m)

    elif call.data == "cat_android":
        m.add(types.InlineKeyboardButton(f"DRIP CLIENT (31 Días) - ${PRECIOS['d31']}", callback_data="buy_d31"))
        bot.edit_message_text("🤖 **ANDROID:**", call.message.chat.id, call.message.message_id, reply_markup=m)

    elif call.data == "cat_cert":
        m.add(types.InlineKeyboardButton(f"COMPRAR CERTIFICADO - ${PRECIOS['cert']}", callback_data="buy_cert"))
        bot.edit_message_text("📜 **SISTEMA DE CERTIFICADOS:**", call.message.chat.id, call.message.message_id, reply_markup=m)

    elif call.data.startswith("buy_"):
        bot.answer_callback_query(call.id, f"❌ Saldo insuficiente. Contacta a @{MI_USER}", show_alert=True)

# --- 7. COMANDOS DE ADMINISTRADOR ---
@bot.message_handler(commands=['autorizar'])
def auth(m):
    if m.from_user.id == ADMIN_ID:
        try:
            nuevo = int(m.text.split()[1])
            if nuevo not in usuarios_autorizados: usuarios_autorizados.append(nuevo)
            bot.reply_to(m, f"✅ ID `{nuevo}` ha sido autorizado.")
        except: bot.reply_to(m, "Uso: `/autorizar ID`", parse_mode="Markdown")

@bot.message_handler(commands=['recargar'])
def recharge(m):
    if m.from_user.id == ADMIN_ID:
        try:
            partes = m.text.split()
            tid, monto = int(partes[1]), float(partes[2])
            saldos[tid] = saldos.get(tid, 0.0) + monto
            bot.send_message(m.chat.id, f"✅ Saldo de `{tid}` actualizado a ${saldos[tid]}")
            bot.send_message(tid, f"💰 ¡Recarga exitosa! Tu nuevo saldo es: ${saldos[tid]}")
        except: bot.reply_to(m, "Uso: `/recargar ID MONTO`", parse_mode="Markdown")

if __name__ == "__main__":
    bot.infinity_polling()
