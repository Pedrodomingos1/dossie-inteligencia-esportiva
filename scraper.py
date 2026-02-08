import requests
import random
from datetime import datetime

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:121.0) Gecko/20100101 Firefox/121.0",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.1 Safari/605.1.15"
]

def obter_cabecalhos():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Referer": "https://www.sofascore.com/",
        "Origin": "https://www.sofascore.com"
    }

def buscar_jogos_do_dia():
    try:
        hoje_str = datetime.now().strftime('%Y-%m-%d')
        url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{hoje_str}"
        resposta = requests.get(url, headers=obter_cabecalhos())
        resposta.raise_for_status()
        dados = resposta.json()
        
        jogos = []
        for evento in dados.get('events', [])[:25]:
            jogos.append({
                'id': evento['id'],
                'nome': f"{evento['homeTeam']['name']} vs {evento['awayTeam']['name']}"
            })
        return jogos
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar jogos do dia: {e}")
        return []
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return []

def buscar_estatisticas_jogo(id_evento):
    try:
        url = f"https://www.sofascore.com/api/v1/event/{id_evento}/statistics"
        resposta = requests.get(url, headers=obter_cabecalhos())
        resposta.raise_for_status()
        dados = resposta.json()
        
        estatisticas = {}
        if 'statistics' in dados:
            for periodo in dados['statistics']:
                if periodo['period'] == 'ALL':
                    for grupo in periodo['groups']:
                        for item in grupo['statisticsItems']:
                            estatisticas[item['name']] = {'casa': item['home'], 'fora': item['away']}
            return estatisticas
        return None
    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar estatísticas do jogo: {e}")
        return None
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return None
