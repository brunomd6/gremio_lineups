import requests
import time

BASE_URL = "https://sports.bzzoiro.com/api"

headers = {
    "Authorization": "Token 910c6099f543922e97dc43c1c70080f4994f2103"
}

LEAGUE_ID = 9
SEASON = 2026

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



detailed_matches = []

for m in gremio_matches:
    match_id = m["id"]
    date = m["event_date"][:10]

    res = requests.get(
        f"{BASE_URL}/events/{match_id}/",
        headers=headers,
        params={
            "date_from": date,
            "date_to": date
        }
    )

    if res.status_code != 200:
        print(f"Failed for ID {match_id}: {res.status_code}")
        continue

    if "application/json" not in res.headers.get("Content-Type", ""):
        print(f"Non-JSON response for ID {match_id}")
        continue

    data = res.json()
    detailed_matches.append(data)

    print(f"✔ Retrieved match {match_id}")

    time.sleep(0.3)  # avoid rate limit

for m in detailed_matches:
    date = m["event_date"][:10]
    home = m["home_team"]
    away = m["away_team"]
    hs = m["home_score"]
    as_ = m["away_score"]
    round_ = m["round_number"]

    score = f"{hs}-{as_}" if hs is not None else "vs"

    print(f"{date} | R{round_:02d} | {home} {score} {away}")

    import json

for m in detailed_matches:
    print(json.dumps(m, indent=2))
    break  # just first match