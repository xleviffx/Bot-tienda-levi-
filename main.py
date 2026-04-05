import telebot
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def enviar_bienvenida(message):
    bot.reply_to(message, "¡Hola! Tu bot de ventas está funcionando.\nPronto agregaremos el sistema de saldos.")

bot.infinity_polling()
