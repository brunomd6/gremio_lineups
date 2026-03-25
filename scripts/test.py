import requests

API_KEY = "YOUR_API_KEY"

BASE_URL = "https://v3.football.api-sports.io"
HEADERS = {
    "x-apisports-key": API_KEY
}

TEAM_ID = 130        # Grêmio
SEASON = 2026
LEAGUE_ID = 71       # Brasileirão (optional but recommended)

# --- Step 1: Check if season exists ---
def season_exists():
    url = f"{BASE_URL}/leagues"
    params = {"id": LEAGUE_ID}

    res = requests.get(url, headers=HEADERS, params=params)
    data = res.json()

    seasons = data["response"][0]["seasons"]
    years = [s["year"] for s in seasons]

    return SEASON in years


# --- Step 2: Fetch all fixtures (with pagination) ---
def get_fixtures():
    url = f"{BASE_URL}/fixtures"
    page = 1
    all_matches = []

    while True:
        params = {
            "team": TEAM_ID,
            "season": SEASON,
            "league": LEAGUE_ID,
            "page": page
        }

        res = requests.get(url, headers=HEADERS, params=params)
        data = res.json()

        matches = data["response"]
        all_matches.extend(matches)

        # pagination info
        current = data["paging"]["current"]
        total = data["paging"]["total"]

        if current >= total:
            break

        page += 1

    return all_matches


# --- Step 3: Print results nicely ---
def print_matches(matches):
    if not matches:
        print("No matches found.")
        return

    for m in matches:
        fixture_id = m["fixture"]["id"]
        date = m["fixture"]["date"][:10]
        home = m["teams"]["home"]["name"]
        away = m["teams"]["away"]["name"]
        goals_home = m["goals"]["home"]
        goals_away = m["goals"]["away"]
        round_name = m["league"]["round"]

        print(f"{date} | {home} vs {away} | {goals_home}-{goals_away} | {round_name} | id={fixture_id}")


# --- MAIN ---
if not season_exists():
    print(f"Season {SEASON} not available in API.")
else:
    matches = get_fixtures()
    print_matches(matches)