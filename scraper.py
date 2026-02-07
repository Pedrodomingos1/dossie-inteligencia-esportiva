import requests
from datetime import datetime

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36"
}

def get_daily_games():
    """Fetches a list of games for the current day from the SofaScore API."""
    try:
        today_str = datetime.now().strftime('%Y-%m-%d')
        url = f"https://www.sofascore.com/api/v1/sport/football/scheduled-events/{today_str}"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        games = []
        for event in data.get('events', [])[:25]:
            games.append({
                'id': event['id'],
                'name': f"{event['homeTeam']['name']} vs {event['awayTeam']['name']}"
            })
        return games
    except requests.exceptions.RequestException as e:
        print(f"Error fetching daily games: {e}")
        return []
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return []

def get_game_statistics(event_id):
    """Fetches detailed statistics for a specific game event from the SofaScore API."""
    try:
        url = f"https://www.sofascore.com/api/v1/event/{event_id}/statistics"
        response = requests.get(url, headers=HEADERS)
        response.raise_for_status()
        data = response.json()
        
        stats = {}
        if 'statistics' in data:
            for period in data['statistics']:
                if period['period'] == 'ALL':
                    for group in period['groups']:
                        for item in group['statisticsItems']:
                            stats[item['name']] = {'home': item['home'], 'away': item['away']}
            return stats
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error fetching game statistics: {e}")
        return None
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        return None
