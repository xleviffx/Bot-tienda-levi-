import telebot
from telebot import types
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# --- 1. CONFIGURACIÓN DEL DUEÑO ---
ADMIN_ID = 8426713423  # <--- CAMBIA ESTO POR TU ID (NÚMERO)
MI_USUARIO_TELEGRAM = "xleviffx" # Tu usuario configurado

# Bases de datos temporales
usuarios_autorizados = []
saldos = {}
historial_keys = {}

# Precios de los productos
PRECIOS = {
    "f31": 18, "f7": 9, "f1": 3,
    "d31": 11, "cert": 5
}

# --- 2. MENÚ PRINCIPAL ---
def menu_principal():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 Mi Perfil", "🛒 Productos")
    markup.add("🔑 Últimas Keys")
    return markup

# --- 3. FILTRO DE ACCESO (BOTÓN A TU TELEGRAM) ---
@bot.message_handler(func=lambda message: message.from_user.id not in usuarios_autorizados and message.from_user.id != ADMIN_ID)
def acceso_denegado(message):
    markup = types.InlineKeyboardMarkup()
    btn_admin = types.InlineKeyboardButton("📩 Contactar Administrador", url=f"https://t.me/{MI_USUARIO_TELEGRAM}")
    markup.add(btn_admin)
    bot.send_message(
        message.chat.id, 
        f"🚫 **ACCESO RESTRINGIDO**\n\nTu ID es: `{message.from_user.id}`\n\nNo tienes acceso permitido. Envía tu ID al administrador para que te autorice y puedas comprar.", 
        reply_markup=markup, 
        parse_mode="Markdown"
    )

# --- 4. COMANDO DE INICIO ---
@bot.message_handler(commands=['start'])
def inicio(message):
    uid = message.from_user.id
    if uid not in saldos:
        saldos[uid] = 0.0
        historial_keys[uid] = []
    bot.send_message(message.chat.id, "✅ Acceso concedido. Bienvenido al Sistema de Ventas.", reply_markup=menu_principal())

# --- 5. LÓGICA DE BOTONES DE TEXTO ---
@bot.message_handler(func=lambda message: True)
def manejar_botones(message):
    uid = message.from_user.id
    if message.text == "👤 Mi Perfil":
        saldo = saldos.get(uid, 0.0)
        user_name = message.from_user.username if message.from_user.username else "Sin Usuario"
        bot.send_message(message.chat.id, f"📌 **TU PERFIL**\n\n👤 Usuario: @{user_name}\n🆔 ID: `{uid}`\n💰 Saldo: ${saldo}", parse_mode="Markdown")

    elif message.text == "🛒 Productos":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("🍎 IOS", callback_data="cat_ios"), types.InlineKeyboardButton("🤖 ANDROID", callback_data="cat_android"))
        markup.add(types.InlineKeyboardButton("💻 PC", callback_data="cat_pc"), types.InlineKeyboardButton("📜 CERTIFICADO", callback_data="cat_cert"))
        bot.send_message(message.chat.id, "🛒 **CATEGORÍAS DISPONIBLES:**", reply_markup=markup, parse_mode="Markdown")

    elif message.text == "🔑 Últimas Keys":
        keys = historial_keys.get(uid, [])
        lista = "\n".join([f"• `{k}`" for k in keys[-5:]]) if keys else "Aún no has realizado compras."
        bot.send_message(message.chat.id, f"🎟 **TUS ÚLTIMAS 5 KEYS:**\n\n{lista}", parse_mode="Markdown")

# --- 6. NAVEGACIÓN DE PRODUCTOS ---
@bot.callback_query_handler(func=lambda call: True)
def interactuar(call):
    m = types.InlineKeyboardMarkup()

    # --- CATEGORÍA IOS ---
    if call.data == "cat_ios":
        m.add(types.InlineKeyboardButton("💎 FLOURITE", callback_data="sub_flourite"))
        bot.edit_message_text("🍎 **PRODUCTOS IOS:**", call.message.chat.id, call.message.message_id, reply_markup=m, parse_mode="Markdown")

    elif call.data == "sub_flourite":
        m.add(types.InlineKeyboardButton(f"📅 31 Días - ${PRECIOS['f31']}", callback_data="buy_f31"))
        m.add(types.InlineKeyboardButton(f"📅 7 Días - ${PRECIOS['f7']}", callback_data="buy_f7"))
        m.add(types.InlineKeyboardButton(f"📅 1 Día - ${PRECIOS['f1']}", callback_data="buy_f1"))
        bot.edit_message_text("💎 **FLOURITE (IOS):**", call.message.chat.id, call.message.message_id, reply_markup=m, parse_mode="Markdown")

    # --- CATEGORÍA ANDROID ---
    elif call.data == "cat_android":
        m.add(types.InlineKeyboardButton(f"🔹 DRIP CLIENT (31 Días) - ${PRECIOS['d31']}", callback_data="buy_d31"))
        bot.edit_message_text("🤖 **PRODUCTOS ANDROID:**", call.message.chat.id, call.message.message_id, reply_markup=m, parse_mode="Markdown")

    # --- CATEGORÍA PC ---
    elif call.data == "cat_pc":
        bot.answer_callback_query(call.id, "Aún no hay productos en PC.")

    # --- CATEGORÍA CERTIFICADO ---
    elif call.data == "cat_cert":
        m.add(types.InlineKeyboardButton(f"📜 COMPRAR CERTIFICADO - ${PRECIOS['cert']}", callback_data="buy_cert"))
        bot.edit_message_text("📜 **SISTEMA DE CERTIFICADOS:**", call.message.chat.id, call.message.message_id, reply_markup=m, parse_mode="Markdown")

    # RESPUESTA AL COMPRAR (SIN SALDO)
    elif call.data.startswith("buy_"):
        bot.answer_callback_query(call.id, "❌ Error: Saldo insuficiente. Contacta a @xleviffx", show_alert=True)

# --- 7. COMANDOS DE ADMINISTRADOR ---
@bot.message_handler(commands=['autorizar'])
def cmd_autorizar(message):
    if message.from_user.id == ADMIN_ID:
        try:
            nuevo_id = int(message.text.split()[1])
            if nuevo_id not in usuarios_autorizados:
                usuarios_autorizados.append(nuevo_id)
            bot.reply_to(message, f"✅ El ID `{nuevo_id}` ahora tiene acceso al bot.", parse_mode="Markdown")
        except:
            bot.reply_to(message, "Uso: `/autorizar ID`", parse_mode="Markdown")

@bot.message_handler(commands=['recargar'])
def cmd_recargar(message):
    if message.from_user.id == ADMIN_ID:
        try:
            _, tid, monto = message.text.split()
            tid, monto = int(tid), float(monto)
            saldos[tid] = saldos.get(tid, 0.0) + monto
            bot.send_message(message.chat.id, f"✅ Saldo de `{tid}` actualizado. Total: ${saldos[tid]}", parse_mode="Markdown")
            bot.send_message(tid, f"💰 **¡Recarga exitosa!** Tu nuevo saldo es: ${saldos[tid]}", parse_mode="Markdown")
        except:
            bot.reply_to(message, "Uso: `/recargar ID MONTO`", parse_mode="Markdown")

bot.infinity_polling()



