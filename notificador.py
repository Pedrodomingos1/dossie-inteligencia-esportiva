import os
import requests

class MensageiroTelegram:
    def __init__(self):
        self.token_bot = os.getenv('TELEGRAM_BOT_TOKEN')
        self.id_chat = os.getenv('TELEGRAM_CHAT_ID')

    def enviar_dossie(self, mensagem):
        if not self.token_bot or not self.id_chat:
            print("Credenciais do Telegram não configuradas.")
            return

        url = f"https://api.telegram.org/bot{self.token_bot}/sendMessage"
        payload = {
            'chat_id': self.id_chat,
            'text': mensagem,
            'parse_mode': 'Markdown'
        }

        try:
            resposta = requests.post(url, json=payload)
            resposta.raise_for_status()
            print("Mensagem enviada para o Telegram com sucesso.")
        except requests.exceptions.RequestException as e:
            print(f"Falha ao enviar mensagem para o Telegram: {e}")
            raise
