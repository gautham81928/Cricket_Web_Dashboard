import os
import requests
from dotenv import load_dotenv

load_dotenv("scraper.env")

API_KEY = os.getenv("CRICAPI_KEY")
BASE_URL = "https://api.cricapi.com/v1/currentMatches"


def get_current_matches():
    """Fetches current matches from CricAPI and returns a list of match dicts."""
    if not API_KEY:
        raise ValueError("CRICAPI_KEY is missing from scraper.env")

    parameters = {
        "apikey": API_KEY,
        "offset": 0
    }

    response = requests.get(BASE_URL, params=parameters, timeout=15)
    response.raise_for_status()
    payload = response.json()

    if payload.get("status") != "success":
        error_msg = payload.get("status", "Unknown API error")
        raise RuntimeError(f"CricAPI error: {error_msg}")

    return payload.get("data", [])


def show_matches(matches):
    if not matches:
        print("No matches found.")
        return

    print(f"\nFound {len(matches)} Current Matches:\n")
    for match in matches:
        name = match.get("name", "Unknown match")
        status = match.get("status", "Unknown status")
        match_type = match.get("matchType", "").upper()

        print(f"Match: {name} [Type: {match_type}]")
        print(f"Status: {status}")

        score_info = match.get("score", [])
        if score_info:
            for inning in score_info:
                team = inning.get("inning", "Inning")
                runs = inning.get("r", 0)
                wickets = inning.get("w", 0)
                overs = inning.get("o", 0)
                print(f"  > {team}: {runs}/{wickets} in {overs} overs")
        else:
            print("  > No live score available yet.")

        print("-" * 40)


if __name__ == "__main__":
    try:
        data = get_current_matches()
        show_matches(data)
    except Exception as err:
        print(f"Error: {err}")