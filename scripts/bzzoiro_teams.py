# 910c6099f543922e97dc43c1c70080f4994f2103

import requests
import json

BASE_URL = "https://sports.bzzoiro.com/api"

headers = {
    "Authorization": "Token 910c6099f543922e97dc43c1c70080f4994f2103"
}

LEAGUE_ID = 9
SEASON = 2026

# --- fetch all pages ---
res = requests.get(
    f"{BASE_URL}/events",
    headers=headers,
    params={
        "date_from": "2026-01-01",
        "date_to": "2026-12-31",
        "league": 9,
        "team": "Grêmio"
    }
)

data = res.json()
matches = data["results"]

print(res.status_code)
print(res.text[:500])

TEAM_ID = 154

gremio_matches = [
    m for m in matches
    if m["home_team_obj"]["id"] == TEAM_ID
    or m["away_team_obj"]["id"] == TEAM_ID
]

for m in gremio_matches:
    date = m["event_date"][:10]
    id = m["id"]
    api_id = m["api_id"]
    home = m["home_team"]
    away = m["away_team"]
    hs = m["home_score"]
    as_ = m["away_score"]
    round_ = m["round_number"]

    print(f"{date} | {id} | {api_id} | {home} vs {away} | {hs}-{as_} | Round {round_}")


match_id = gremio_matches[0]["id"]
date = gremio_matches[0]["event_date"][:10]

res = requests.get(
    f"{BASE_URL}/events/{match_id}/",
    headers=headers,
    params={
        "date_from": date,
        "date_to": date
    }
)

print(res.status_code)
print(res.text[:500])
