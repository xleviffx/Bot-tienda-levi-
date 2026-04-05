import telebot
from telebot import types
import os

# CONFIGURACIÓN
TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)
ADMIN_ID = 8426713423  # TU ID

@bot.message_handler(commands=['start'])
def inicio(m):
    uid = m.from_user.id
    if uid == ADMIN_ID:
        bot.send_message(m.chat.id, "👑 **BIENVENIDO JEFE**", parse_mode="Markdown")
    
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add("👤 Mi Perfil", "🛒 Productos")
    bot.send_message(m.chat.id, "✅ Sistema Activo", reply_markup=markup)

@bot.message_handler(func=lambda m: True)
def echo_all(m):
    if m.text == "👤 Mi Perfil":
        bot.reply_to(m, f"📌 Usuario: @{m.from_user.username}\n💰 Saldo: $0.0")

if __name__ == "__main__":
    bot.infinity_polling()
