import logging
from bot import iniciar_bot

logging.basicConfig(level=logging.INFO)
logging.info("Bot iniciado! Aguardando mensagens...")

iniciar_bot()  # This is the command that starts the bot
