# 910c6099f543922e97dc43c1c70080f4994f2103

import requests
import json

BASE_URL = "https://sports.bzzoiro.com/api"

headers = {
    "Authorization": "Token 910c6099f543922e97dc43c1c70080f4994f2103"
}

LEAGUE_ID = 9
SEASON = 2026
TEAM_ID = 154
TEAM_API_ID = 5926

# --- fetch all pages ---
url = f"{BASE_URL}/events"
params = {
    "league": LEAGUE_ID,
    "season": SEASON
}

all_matches = []

while url:
    res = requests.get(url, headers=headers, params=params if url.endswith("/events") else None)

    if res.status_code != 200:
        print("Request failed:", res.status_code)
        print(res.text)
        break

    if "application/json" not in res.headers.get("Content-Type", ""):
        print("Not JSON response")
        print(res.text[:500])
        break

    data = res.json()

    all_matches.extend(data["results"])

    # pagination
    url = data["next"]
    params = None  # only needed for first request


for m in all_matches[:20]:
    print(m["home_team"], "vs", m["away_team"])

# --- filter Grêmio ---
gremio_matches = [
    m for m in all_matches
    if "Grêmio" in m["home_team"].lower()
    or "Grêmio" in m["away_team"].lower()
]

# --- print nicely ---
for m in gremio_matches:
    date = m["event_date"][:10]
    home = m["home_team"]
    away = m["away_team"]
    hs = m["home_score"]
    as_ = m["away_score"]
    round_ = m["round_number"]
    fixture_id = m["id"]

    print(f"{date} | {home} vs {away} | {hs}-{as_} | Round {round_} | id={fixture_id}")