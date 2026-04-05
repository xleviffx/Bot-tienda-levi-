import telebot
import os

TOKEN = os.environ.get('BOT_TOKEN')
bot = telebot.TeleBot(TOKEN)

# Diccionario para guardar saldos (ID del usuario: Dinero)
saldos = {}

# Lista de códigos disponibles (Esto es lo que venderás)
codigos_netflix = ["NET-123-ABC", "NET-456-DEF", "NET-789-GHI"]
PRECIO_NETFLIX = 5.0  # Precio de cada código

@bot.message_handler(commands=['start'])
def bienvenida(message):
    user_id = message.from_user.id
    if user_id not in saldos:
        saldos[user_id] = 0.0  # Empiezan con 0
    bot.reply_to(message, f"¡Bienvenido a la Tienda! 🛒\n\n💰 Tu saldo: ${saldos[user_id]}\n\nComandos:\n/perfil - Ver tu cuenta\n/comprar - Ver productos\n/recargar - Cómo añadir saldo")

@bot.message_handler(commands=['perfil'])
def ver_perfil(message):
    user_id = message.from_user.id
    saldo = saldos.get(user_id, 0.0)
    bot.send_message(message.chat.id, f"👤 Usuario: {message.from_user.first_name}\n💳 Saldo: ${saldo}")

@bot.message_handler(commands=['comprar'])
def tienda(message):
    bot.send_message(message.chat.id, f"📦 **Productos Disponibles:**\n\n1. Tarjeta Netflix - ${PRECIO_NETFLIX}\n\nEscribe /pago_netflix para comprar una.")

@bot.message_handler(commands=['pago_netflix'])
def comprar_netflix(message):
    user_id = message.from_user.id
    saldo_actual = saldos.get(user_id, 0.0)
    
    if saldo_actual >= PRECIO_NETFLIX:
        if len(codigos_netflix) > 0:
            # Restar saldo
            saldos[user_id] -= PRECIO_NETFLIX
            # Entregar código
            codigo = codigos_netflix.pop(0)
            bot.send_message(message.chat.id, f"✅ ¡Compra exitosa!\n\n🎟 Tu código es: `{codigo}`\n💰 Nuevo saldo: ${saldos[user_id]}")
        else:
            bot.send_message(message.chat.id, "❌ Lo sentimos, no hay stock de este código.")
    else:
        bot.send_message(message.chat.id, f"❌ Saldo insuficiente. Necesitas ${PRECIO_NETFLIX} y tienes ${saldo_actual}.")

bot.infinity_polling()

