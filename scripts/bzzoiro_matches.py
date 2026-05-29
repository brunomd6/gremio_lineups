import requests
import time
import json

BASE_URL = "https://sports.bzzoiro.com/api"

headers = {
    "Authorization": "Token 910c6099f543922e97dc43c1c70080f4994f2103"
}

TEAM_ID = 154

# ----------------------------------------
# get all matches
# ----------------------------------------

res = requests.get(
    f"{BASE_URL}/events/",
    headers=headers,
    params={
        "team_id": TEAM_ID,
        "date_from": "2026-01-01",
        "date_to": "2026-12-31"
    }
)

data = res.json()

matches = data["results"]

print(f"Found {len(matches)} matches")

# ----------------------------------------
# fetch details
# ----------------------------------------

full_dataset = []

for m in matches:
    match_id = m["id"]

    print(f"Fetching {match_id}")

    res = requests.get(
        f"{BASE_URL}/events/{match_id}/",
        headers=headers
    )

    print("STATUS:", res.status_code)

    if res.status_code != 200:
        continue

    detailed = res.json()

    full_dataset.append(detailed)

    time.sleep(0.3)

# ----------------------------------------
# save everything
# ----------------------------------------

with open("./data/gremio_2026_detailed.json", "w", encoding="utf-8") as f:
    json.dump(
        full_dataset,
        f,
        indent=2,
        ensure_ascii=False
    )

print("Saved to gremio_2026_detailed.json")