import requests
import os
from dotenv import load_dotenv

load_dotenv()

class TelegramMessenger:
    def __init__(self):
        self.token = os.getenv("TELEGRAM_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def enviar_dossie(self, mensagem):
        payload = {
            "chat_id": self.chat_id,
            "text": mensagem,
            "parse_mode": "Markdown"
        }
        
        try:
            response = requests.post(self.base_url, data=payload)
            return response.status_code == 200
        except Exception as e:
            print(f"Erro: {e}")
            return False