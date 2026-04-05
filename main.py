import telebot
from telebot import types
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- CONFIGURACIÓN (CAMBIA TU ID AQUÍ) ---
ADMIN_ID = 123456789  # <--- TU ID DE USERINFOBOT
usuarios_autorizados = [] # Lista de IDs con permiso
saldos = {}
historial_keys = {}

# --- LISTA DE PRODUCTOS Y PRECIOS ---
# (Luego te enseñaré a cargar los códigos reales)
PRECIOS = {
    "flourite_31": 18,
    "flourite_7": 9,
    "flourite_1": 3,
    "drip_31": 11,
    "certificado": 5
}

# --- MENÚ PRINCIPAL (BOTONES DE ABAJO) ---
def menu_principal():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 Mi Perfil", "🛒 Productos")
    markup.add("🔑 Últimas Keys")
    return markup

# --- FILTRO DE ACCESO ---
@bot.message_handler(func=lambda message: message.from_user.id not in usuarios_autorizados and message.from_user.id != ADMIN_ID)
def acceso_denegado(message):
    bot.send_message(message.chat.id, f"🚫 **ACCESO RESTRINGIDO**\n\nTu ID: `{message.from_user.id}`\nEnvíalo al admin para que te dé acceso.")

@bot.message_handler(commands=['start'])
def inicio(message):
    user_id = message.from_user.id
    if user_id not in saldos:
        saldos[user_id] = 0.0
        historial_keys[user_id] = []
    bot.send_message(message.chat.id, "✅ Bienvenido al Sistema.", reply_markup=menu_principal())

# --- MANEJO DE BOTONES DE TEXTO ---
@bot.message_handler(func=lambda message: True)
def botones_texto(message):
    uid = message.from_user.id
    
    if message.text == "👤 Mi Perfil":
        saldo = saldos.get(uid, 0.0)
        bot.send_message(message.chat.id, f"📌 **PERFIL**\n👤 Usuario: @{message.from_user.username}\n💰 Saldo: ${saldo}")

    elif message.text == "🛒 Productos":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🍎 IOS", callback_data="cat_ios"))
        markup.add(types.InlineKeyboardButton("🤖 ANDROID", callback_data="cat_android"))
        markup.add(types.InlineKeyboardButton("💻 PC", callback_data="cat_pc"))
        markup.add(types.InlineKeyboardButton("📜 CERTIFICADO", callback_data="cat_cert"))
        bot.send_message(message.chat.id, "Selecciona una categoría:", reply_markup=markup)

    elif message.text == "🔑 Últimas Keys":
        keys = historial_keys.get(uid, [])
        lista = "\n".join([f"• `{k}`" for k in keys[-5:]]) if keys else "No tienes compras."
        bot.send_message(message.chat.id, f"🎟 **TUS ÚLTIMAS 5 KEYS:**\n\n{lista}")

# --- MANEJO DE SUBMENÚS (CALLBACKS) ---
@bot.callback_query_handler(func=lambda call: True)
def respuestas_botones(call):
    markup = types.InlineKeyboardMarkup()
    
    if call.data == "cat_ios":
        markup.add(types.InlineKeyboardButton("💎 FLOURITE", callback_data="prod_flourite"))
        bot.edit_message_text("Has elegido IOS. Selecciona un software:", call.message.chat.id, call.message.message_id, reply_markup=markup)
    
    elif call.data == "prod_flourite":
        markup.add(types.InlineKeyboardButton(f"31 Días - ${PRECIOS['flourite_31']}", callback_data="buy_f31"))
        markup.add(types.InlineKeyboardButton(f"7 Días - ${PRECIOS['flourite_7']}", callback_data="buy_f7"))
        markup.add(types.InlineKeyboardButton(f"1 Día - ${PRECIOS['flourite_1']}", callback_data="buy_f1"))
        bot.edit_message_text("FLOURITE - Selecciona la duración:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "cat_android":
        markup.add(types.InlineKeyboardButton(f"DRIP CLIENT (31 Días) - ${PRECIOS['drip_31']}", callback_data="buy_d31"))
        bot.edit_message_text("Has elegido ANDROID:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    elif call.data == "cat_cert":
        markup.add(types.InlineKeyboardButton(f"Comprar Certificado - ${PRECIOS['certificado']}", callback_data="buy_cert"))
        bot.edit_message_text("CERTIFICADOS:", call.message.chat.id, call.message.message_id, reply_markup=markup)

    # Lógica de compra (Ejemplo rápido)
    elif call.data.startswith("buy_"):
        bot.answer_callback_query(call.id, "Procesando compra... (Necesitas saldo)")

bot.infinity_polling()


