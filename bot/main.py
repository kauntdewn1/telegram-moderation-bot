import logging
from telegram.ext import Updater, CommandHandler

def iniciar_bot():
    logging.basicConfig(level=logging.INFO)
    print("Bot iniciado! Aguardando mensagens...")

    # Pegue o token do bot do arquivo .env (ou substitua pelo seu token diretamente)
    import os
    TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")  # Certifique-se de ter um .env configurado

    if not TOKEN:
        print("Erro: O token do bot não foi encontrado. Verifique o arquivo .env")
        return

    updater = Updater(TOKEN, use_context=True)
    dispatcher = updater.dispatcher

    def start(update, context):
        update.message.reply_text("Olá! Eu sou o bot moderador!")

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()
