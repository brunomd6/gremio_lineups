from datetime import datetime, timezone

def find_bzz_match(match, bzz_matches):

    target_date = match["date"]

    for b in bzz_matches:

        b_date = normalized_bzz_date(
            b["event_date"]
        )

        if b_date == target_date:
            return b

    return None

def normalized_bzz_date(event_date: str) -> str:

    dt = datetime.fromisoformat(event_date)

    dt = dt.astimezone(timezone.utc)

    return dt.strftime("%Y-%m-%d")