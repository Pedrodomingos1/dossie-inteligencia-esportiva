import os
import requests

class TelegramMessenger:
    def __init__(self):
        self.bot_token = os.getenv('TELEGRAM_BOT_TOKEN')
        self.chat_id = os.getenv('TELEGRAM_CHAT_ID')

    def enviar_dossie(self, mensagem):
        """Envies a message to the configured Telegram chat."""
        if not self.bot_token or not self.chat_id:
            print("Telegram credentials not configured.")
            return

        url = f"https://api.telegram.org/bot{self.bot_token}/sendMessage"
        payload = {
            'chat_id': self.chat_id,
            'text': mensagem,
            'parse_mode': 'Markdown'
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("Message sent to Telegram successfully.")
        except requests.exceptions.RequestException as e:
            print(f"Failed to send message to Telegram: {e}")
            raise
