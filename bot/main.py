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

# /start - Iniciar o bot
async def start(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("🤖 Bot iniciado! Use /help para ver os comandos disponíveis.")

# /regras - Mostrar as regras do chat
async def regras(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("📜 Regras do chat:\n"
                                    "1️⃣ Respeite todos os membros.\n"
                                    "2️⃣ Não envie links suspeitos.\n"
                                    "3️⃣ Proibido spam e mensagens ofensivas.\n"
                                    "4️⃣ Siga as diretrizes da comunidade.\n\n"
                                    "❗ O não cumprimento pode resultar em banimento.")

# /help - Mostrar os comandos disponíveis
async def help(update: Update, context: CallbackContext) -> None:
    await update.message.reply_text("ℹ️ Comandos disponíveis:\n"
                                    "/start - Iniciar o bot\n"
                                    "/regras - Mostrar as regras do chat\n"
                                    "/ban - Banir um usuário (somente admin)\n"
                                    "/mute - Silenciar um usuário (somente admin)\n"
                                    "/unmute - Desmutar um usuário (somente admin)\n"
                                    "/warn - Avisar um usuário (somente admin)\n"
                                    "/help - Mostrar esta mensagem de ajuda")

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
    # Adiciona o handler para o comando /regras que mostra as regras do chat
    app.add_handler(CommandHandler("regras", regras))
    app.add_handler(CommandHandler("help", help))
    app.add_handler(CommandHandler("ban", ban))
    app.add_handler(CommandHandler("mute", mute))
    app.add_handler(CommandHandler("unmute", unmute))
    app.add_handler(CommandHandler("warn", warn))

    # Rodando o bot
    app.run_polling()
