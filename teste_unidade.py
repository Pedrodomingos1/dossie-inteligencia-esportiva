import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notificador import TelegramMessenger
from dotenv import load_dotenv
from unittest.mock import MagicMock

load_dotenv()

def verificar_sistema():
    print("⚔️ Iniciando Teste de Integridade...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        # In a CI/CD or docker environment, selenium setup might need specific paths or drivers.
        # For this test script, we assume a basic setup or we can mock it if driver fails.
        driver = webdriver.Chrome(options=chrome_options)
        driver.quit()
        print("✅ Selenium: Operacional")
    except Exception as e:
        print(f"❌ Selenium: Falha - {e}")
        # Proceed even if selenium fails, to test notifier

    mensageiro = TelegramMessenger()

    # Mock the actual sending part if credentials are not present or for testing purposes
    if not os.getenv('TELEGRAM_BOT_TOKEN') or not os.getenv('TELEGRAM_CHAT_ID'):
        print("⚠️  Telegram Credentials missing. Mocking the send operation.")
        mensageiro.enviar_dossie = MagicMock(return_value=None)

    agora = datetime.datetime.now().strftime("%H:%M:%S")
    teste_msg = f"🛡️ *Teste de Sistema*\nStatus: Operacional\nHorário: {agora}"
    
    try:
        mensageiro.enviar_dossie(teste_msg)
        print("✅ Notificador: Mensagem enviada ao Telegram (ou Mock)")
    except Exception as e:
        print(f"❌ Notificador: Falha - {e}")

if __name__ == "__main__":
    verificar_sistema()
