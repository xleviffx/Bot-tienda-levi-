 callback_data="buy_f7"))
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

bot.infinity_polling



