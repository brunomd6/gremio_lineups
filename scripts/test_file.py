from pathlib import Path

path = Path("../data/bzzoiro_gremio_2026_detailed.json")

if path.exists():
    print("Exists")
else:
    print("Does not exist")

