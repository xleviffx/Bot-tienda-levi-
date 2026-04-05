_id}` ahora tiene acceso al bot.", parse_mode="Markdown")
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

bot.infinity_polling
