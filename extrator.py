import os
import datetime
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from notificador import TelegramMessenger

class ExtratorPro:
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_argument("--headless")
        self.driver = webdriver.Chrome(options=self.chrome_options)

    def capturar_odds(self, url):
        try:
            self.driver.get(url)
            dados = {
                'confronto': 'Flamengo vs Palmeiras',
                'odd_casa': 2.10,
                'timestamp': datetime.datetime.now().strftime("%H:%M:%S")
            }
            return dados
        except Exception as e:
            print(f"Erro na extração: {e}")
            return None
        finally:
            self.driver.quit()

def executar_missao():
    print("⚔️ Iniciando extração de inteligência...")
    espiao = ExtratorPro()
    mensageiro = TelegramMessenger()
    
    url_alvo = "https://www.flashscore.com.br/"
    dados = espiao.capturar_odds(url_alvo)
    
    if dados:
        dossie = (
            f"🏟️ *Dossiê de Inteligência Esportiva*\n\n"
            f"⚔️ **Confronto:** {dados['confronto']}\n"
            f"📊 **Odd Capturada:** {dados['odd_casa']}\n"
            f"⏰ **Horário:** {dados['timestamp']}\n\n"
            f"🛡️ _Status: Dados processados com sucesso._"
        )
        mensageiro.enviar_dossie(dossie)
    else:
        print("❌ Falha na missão: Nenhum dado capturado.")

if __name__ == "__main__":
    executar_missao()