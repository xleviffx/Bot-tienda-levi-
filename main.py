import telebot
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "👑 ¡ESTOY VIVO! El bot funciona correctamente.")

if __name__ == "__main__":
    bot.infinity_polling()
