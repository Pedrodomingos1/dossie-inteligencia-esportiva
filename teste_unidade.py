import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notificador import MensageiroTelegram
from dotenv import load_dotenv
from unittest.mock import MagicMock

load_dotenv()

def verificar_sistema():
    print("⚔️ Iniciando Teste de Integridade...")
    try:
        opcoes_chrome = Options()
        opcoes_chrome.add_argument("--headless")
        opcoes_chrome.add_argument("--no-sandbox")
        opcoes_chrome.add_argument("--disable-dev-shm-usage")
        driver = webdriver.Chrome(options=opcoes_chrome)
        driver.quit()
        print("✅ Selenium: Operacional")
    except Exception as e:
        print(f"❌ Selenium: Falha - {e}")

    mensageiro = MensageiroTelegram()

    if not os.getenv('TELEGRAM_BOT_TOKEN') or not os.getenv('TELEGRAM_CHAT_ID'):
        print("⚠️  Credenciais do Telegram ausentes. Simulando envio.")
        mensageiro.enviar_dossie = MagicMock(return_value=None)

    agora = datetime.datetime.now().strftime("%H:%M:%S")
    mensagem_teste = f"🛡️ *Teste de Sistema*\nStatus: Operacional\nHorário: {agora}"
    
    try:
        mensageiro.enviar_dossie(mensagem_teste)
        print("✅ Notificador: Mensagem enviada ao Telegram (ou Simulação)")
    except Exception as e:
        print(f"❌ Notificador: Falha - {e}")

if __name__ == "__main__":
    verificar_sistema()
