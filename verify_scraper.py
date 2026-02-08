from scraper import get_daily_games, get_game_statistics
import json

def verify_scraper():
    print("Testing get_daily_games()...")
    games = get_daily_games()
    print(f"Games found: {len(games)}")
    if games:
        print(f"First game: {games[0]}")
        event_id = games[0]['id']
        print(f"\nTesting get_game_statistics({event_id})...")
        stats = get_game_statistics(event_id)
        if stats:
             print("Statistics retrieved successfully.")
             # print(json.dumps(stats, indent=2)) # Too verbose
        else:
             print("Failed to retrieve statistics or no statistics available yet.")
    else:
        print("No games found for today.")

if __name__ == "__main__":
    verify_scraper()
