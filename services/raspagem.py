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

def gerar_dados_mock_kpi():
    """Gera dados KPIs simulados para um jogo."""
    confianca = random.randint(3, 5)
    return {
        'probabilidade_ia': random.randint(55, 92),
        'confianca': confianca,
        'tendencia': random.choice([
            "85% de chance de Over 1.5",
            "Mandante marca primeiro em 70% dos jogos",
            "Alta probabilidade de Ambas Marcam",
            "Visitante sofre gols nos últimos 15 min",
            "Tendência forte para Canto HT"
        ]),
        'momentum': [random.randint(20, 90) for _ in range(10)]
    }

def buscar_jogos_do_dia():
    try:
        hoje_str = datetime.now().strftime('%Y-%m-%d')
        url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{hoje_str}"
        resposta = requests.get(url, headers=obter_cabecalhos(), timeout=10)
        resposta.raise_for_status()
        dados = resposta.json()
        
        jogos = []
        for evento in dados.get('events', [])[:25]:
            kpis = gerar_dados_mock_kpi()
            jogos.append({
                'id': evento['id'],
                'nome': f"{evento['homeTeam']['name']} vs {evento['awayTeam']['name']}",
                'homeTeam': evento['homeTeam']['name'],
                'awayTeam': evento['awayTeam']['name'],
                'status': 'live' if evento.get('status', {}).get('type') == 'inprogress' else 'scheduled',
                'time': datetime.fromtimestamp(evento.get('startTimestamp', 0)).strftime('%H:%M'),
                **kpis
            })

        if not jogos:
            raise ValueError("API retornou lista vazia")

        return jogos

    except (requests.exceptions.RequestException, ValueError) as e:
        print(f"Erro ao buscar jogos do dia (Usando Fallback): {e}")
        # Fallback com dados mock KPIs
        return [
            {'id': 111, 'nome': 'Flamengo vs Vasco', 'homeTeam': 'Flamengo', 'awayTeam': 'Vasco', 'status': 'live', 'time': '16:00', **gerar_dados_mock_kpi(), 'confianca': 5, 'tendencia': 'Flamengo pressionando muito (70% posse)'},
            {'id': 222, 'nome': 'Real Madrid vs Barcelona', 'homeTeam': 'Real Madrid', 'awayTeam': 'Barcelona', 'status': 'scheduled', 'time': '17:00', **gerar_dados_mock_kpi(), 'confianca': 5},
            {'id': 333, 'nome': 'Manchester City vs Liverpool', 'homeTeam': 'Manchester City', 'awayTeam': 'Liverpool', 'status': 'live', 'time': '12:30', **gerar_dados_mock_kpi()},
            {'id': 444, 'nome': 'PSG vs Marseille', 'homeTeam': 'PSG', 'awayTeam': 'Marseille', 'status': 'scheduled', 'time': '20:00', **gerar_dados_mock_kpi()},
            {'id': 555, 'nome': 'Palmeiras vs Corinthians', 'homeTeam': 'Palmeiras', 'awayTeam': 'Corinthians', 'status': 'scheduled', 'time': '18:30', **gerar_dados_mock_kpi()}
        ]
    except Exception as e:
        print(f"Erro inesperado: {e}")
        return []

def buscar_estatisticas_jogo(id_evento):
    try:
        url = f"https://www.sofascore.com/api/v1/event/{id_evento}/statistics"
        resposta = requests.get(url, headers=obter_cabecalhos(), timeout=10)
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

def buscar_odds_simuladas(id_evento):
    """
    Simula odds para um evento, já que a API de odds não é acessível publicamente sem autenticação.
    Retorna odds em formato decimal (float).
    """
    return {
        'casa': round(random.uniform(1.5, 3.5), 2),
        'empate': round(random.uniform(2.8, 4.0), 2),
        'fora': round(random.uniform(2.0, 5.0), 2)
    }
