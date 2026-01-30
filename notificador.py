import os
import requests
from dotenv import load_dotenv

load_dotenv()

class TelegramMessenger:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def enviar_dossie(self, chat_id, mensagem):
        payload = {
            "chat_id": chat_id,
            "text": mensagem,
            "parse_mode": "Markdown"
        }
        try:
            response = requests.post(self.base_url, data=payload)
            return response.status_code == 200
        except:
            return False