from datetime import datetime, timezone

def find_bzz_match(match, bzz_matches):

    target_id = match.get("bzzoiro_id")

    if not target_id:
        return None

    for b in bzz_matches:
        if b.get("id") == target_id:
            return b

    return None

# def normalized_bzz_date(event_date: str) -> str:

#     dt = datetime.fromisoformat(event_date)

#     dt = dt.astimezone(timezone.utc)

#     return dt.strftime("%Y-%m-%d")