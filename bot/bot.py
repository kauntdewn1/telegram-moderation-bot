import logging
from telegram.ext import Updater, CommandHandler

def iniciar_bot():
    logging.basicConfig(level=logging.INFO)
    print("Bot iniciado! Aguardando mensagens...")

    updater = Updater("SEU_TOKEN_AQUI", use_context=True)
    dispatcher = updater.dispatcher

    def start(update, context):
        update.message.reply_text("Olá! Eu sou o bot moderador!")

    dispatcher.add_handler(CommandHandler("start", start))

    updater.start_polling()
    updater.idle()
