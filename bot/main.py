import logging
import os
from telegram import Update, ChatPermissions
from telegram.ext import Application, CommandHandler, CallbackContext

# Verifica se o usuário que enviou o comando é admin
async def is_admin(update: Update) -> bool:
    chat_member = await update.effective_chat.get_member(update.effective_user.id)
    return chat_member.status in ["administrator", "creator"]

# /ban - Banir um usuário (somente admin)
async def ban(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update):
        await update.message.reply_text("⚠️ Você não tem permissão para usar este comando.")
        return

    if not context.args:
        await update.message.reply_text("❌ Você precisa marcar um usuário ou informar um ID para banir.")
        return

    try:
        user_id = int(context.args[0])
        await context.bot.ban_chat_member(update.effective_chat.id, user_id)
        await update.message.reply_text(f"✅ Usuário {user_id} foi banido!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao banir: {e}")

# /mute - Silenciar um usuário (somente admin)
async def mute(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update):
        await update.message.reply_text("⚠️ Você não tem permissão para usar este comando.")
        return

    if not context.args:
        await update.message.reply_text("❌ Você precisa marcar um usuário ou informar um ID para silenciar.")
        return

    try:
        user_id = int(context.args[0])
        await context.bot.restrict_chat_member(
            update.effective_chat.id, user_id, ChatPermissions()
        )
        await update.message.reply_text(f"🔇 Usuário {user_id} foi silenciado!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao silenciar: {e}")

# /unmute - Desmutar um usuário (somente admin)
async def unmute(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update):
        await update.message.reply_text("⚠️ Você não tem permissão para usar este comando.")
        return

    if not context.args:
        await update.message.reply_text("❌ Você precisa marcar um usuário ou informar um ID para desmutar.")
        return

    try:
        user_id = int(context.args[0])
        await context.bot.restrict_chat_member(
            update.effective_chat.id, user_id, ChatPermissions(can_send_messages=True)
        )
        await update.message.reply_text(f"🔊 Usuário {user_id} foi desmutado!")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao desmutar: {e}")

# /warn - Avisar um usuário (somente admin)
async def warn(update: Update, context: CallbackContext) -> None:
    if not await is_admin(update):
        await update.message.reply_text("⚠️ Você não tem permissão para usar este comando.")
        return

    if not context.args:
        await update.message.reply_text("❌ Você precisa marcar um usuário ou informar um ID para avisar.")
        return

    try:
        user_id = int(context.args[0])
        await update.message.reply_text(f"⚠️ Aviso enviado para o usuário {user_id}.")
    except Exception as e:
        await update.message.reply_text(f"❌ Erro ao enviar aviso: {e}")

# Função para iniciar o bot
def iniciar_bot():
    logging.basicConfig(level=logging.INFO)
    print("Bot iniciado! Aguardando mensagens...")

    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not TOKEN:
        print("Erro: O token do bot não foi encontrado. Verifique o arquivo .env")
        return

    # Criando a aplicação
    app = Application.builder().token(TOKEN).build()

    # Adicionando handlers de comandos
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("regras", regras))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("warn", warn))

    # Rodando o bot
    app.run_polling()
