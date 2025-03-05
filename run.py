import logging
from bot import iniciar_bot  # Verifique se esse import está correto

logging.basicConfig(level=logging.INFO)
print("Bot iniciado! Aguardando mensagens...")

iniciar_bot()  # Esse é o comando que inicia o bot
