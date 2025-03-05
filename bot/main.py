import logging
import os
from telegram import Update, ChatPermissions, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, CallbackContext, filters

# Mensagem de boas-vindas com botões interativos
async def boas_vindas(update: Update, context: CallbackContext) -> None:
    for user in update.message.new_chat_members:
        keyboard = [
            [InlineKeyboardButton("📜 Regras do Grupo", callback_data="regras")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)

        await update.message.reply_text(
            f"🎉 Bem-vindo, {user.first_name}! 🚀\n\n"
            "Aqui estão algumas informações importantes para você começar:",
            reply_markup=reply_markup
        )


# Handler de boas-vindas ao grupo
app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, boas_vindas))

# Função para responder ao botão das regras
async def botao_clicado(update: Update, context: CallbackContext) -> None:
    query = update.callback_query
    if query.data == "regras":
        await query.message.reply_text("📜 **Regras do Grupo:**\n1. Respeite todos.\n2. Sem spam.\n3. Seja ativo!")

# Lista de palavras proibidas (adapte conforme necessário)
PALAVRAS_PROIBIDAS = ["spam", "scam", "fraude", "clique aqui", "dinheiro fácil"]

# Função de verificação de mensagens (AntiSpam)
async def verificar_mensagem(update: Update, context: CallbackContext) -> None:
    mensagem = update.message.text.lower()
    palavras_proibidas = ["spam", "fraude", "dinheiro fácil"]

    if any(palavra in mensagem for palavra in palavras_proibidas):
        await update.message.delete()
        await update.message.reply_text(f"⚠️ {update.message.from_user.first_name}, sua mensagem foi removida por conter conteúdo proibido!")

            # Se a mensagem contém links e não é de um admin, remove
    if "http" in mensagem or ".com" in mensagem:
        chat_member = await context.bot.get_chat_member(update.effective_chat.id, update.effective_user.id)
        if chat_member.status not in ["administrator", "creator"]:
            await update.message.delete()
            await update.message.reply_text(f"🚫 {update.message.from_user.first_name}, links não são permitidos no grupo!")
            
            # Adicionar filtro de mensagens no `iniciar_bot`
app.add_handler(MessageHandler(filters.TEXT & ~filters.Command(), verificar_mensagem))

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

# Função principal para iniciar o bot
def iniciar_bot():
    logging.basicConfig(level=logging.INFO)
    print("Bot iniciado! Aguardando mensagens...")

    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

    if not TOKEN:
        print("Erro: O token do bot não foi encontrado. Verifique o arquivo .env")
        return

    # Criando o aplicativo do bot
    app = Application.builder().token(TOKEN).build()

    # Adicionando os handlers ao bot
    app.add_handler(MessageHandler(filters.TEXT & ~filters.Command(), verificar_mensagem))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, boas_vindas))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, boas_vindas))
    app.add_handler(CommandHandler("regras", botao_clicado))

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

# Rodar o bot apenas se este arquivo for executado diretamente
if __name__ == "__main__":
    iniciar_bot()
