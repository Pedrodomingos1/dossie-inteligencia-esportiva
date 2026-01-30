import requests
from datetime import datetime

class ExtratorEstatistico:
    def __init__(self):
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
        }

    def listar_jogos_hoje(self):
        try:
            hoje = datetime.now().strftime('%Y-%m-%d')
            url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{hoje}"
            data = requests.get(url, headers=self.headers).json()
            
            jogos = []
            for ev in data.get('events', [])[:15]:
                jogos.append({
                    'id': ev['id'],
                    'nome': f"{ev['homeTeam']['name']} x {ev['awayTeam']['name']}"
                })
            return jogos
        except:
            return []

    def buscar_dossie_real(self, event_id):
        try:
            url = f"https://www.sofascore.com/api/v1/event/{event_id}/statistics"
            data = requests.get(url, headers=self.headers).json()
            
            resumo = ""
            if 'statistics' in data:
                for period in data['statistics']:
                    if period['period'] == 'ALL':
                        for group in period['groups']:
                            for item in group['statisticsItems']:
                                if item['name'] == 'Corner kicks':
                                    resumo += f"🚩 Escanteios: {item['home']} para o mandante e {item['away']} para o visitante\n"
                                elif item['name'] == 'Ball possession':
                                    resumo += f"⚽ Posse de bola: {item['home']} vs {item['away']}\n"
                                elif item['name'] == 'Expected goals':
                                    resumo += f"📈 Expectativa de gols: {item['home']} contra {item['away']}\n"
                return resumo
            return "As informações detalhadas deste jogo ainda não estão disponíveis no momento."
        except:
            return "Houve um problema ao buscar os dados. Tente novamente em instantes."