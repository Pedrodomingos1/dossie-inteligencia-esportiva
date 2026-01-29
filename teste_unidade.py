import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notificador import TelegramMessenger
from dotenv import load_dotenv

load_dotenv()

def verificar_sistema():
    print("⚔️ Iniciando Teste de Integridade...")
    try:
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        driver = webdriver.Chrome(options=chrome_options)
        driver.quit()
        print("✅ Selenium: Operacional")
    except Exception as e:
        print(f"❌ Selenium: Falha - {e}")
        return

    mensageiro = TelegramMessenger()
    agora = datetime.datetime.now().strftime("%H:%M:%S")
    teste_msg = f"🛡️ *Teste de Sistema*\nStatus: Operacional\nHorário: {agora}"
    
    try:
        mensageiro.enviar_dossie(teste_msg)
        print("✅ Notificador: Mensagem enviada ao Telegram")
    except Exception as e:
        print(f"❌ Notificador: Falha - {e}")

if __name__ == "__main__":
    verificar_sistema()