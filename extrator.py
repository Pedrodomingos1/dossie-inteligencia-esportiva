import os
from notificador import TelegramMessenger

def executar_missao():
    print("⚔️ Iniciando extração de inteligência...")
    espiao = ExtratorPro()
    mensageiro = TelegramMessenger()
    
    # URL de exemplo (substitua pela real do seu alvo)
    url_alvo = "https://www.flashscore.com.br/"
    
    dados = espiao.capturar_odds(url_alvo)
    
    if dados:
        # Formatando o Dossiê para o Telegram
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