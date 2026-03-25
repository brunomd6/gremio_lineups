import requests
import json

API_KEY = "7f4dde750244baf0de99f145dff23a7a"
fixture_id = 1032456

url = "https://v3.football.api-sports.io/fixtures"
headers = {"x-apisports-key": API_KEY}
params = {
    "team": 130,
    "season": 2025
}

res = requests.get(url, headers=headers, params=params)
data = res.json()["response"]

match = data[1]

fixture_id = match["fixture"]["id"]
home = match["teams"]["home"]["name"]
away = match["teams"]["away"]["name"]

print(fixture_id, home, "vs", away)
