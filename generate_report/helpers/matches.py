from helpers.constants import ROUND_NAMES

def get_round_name(round_value):

    try:
        r = int(round_value)

        if 1 <= r <= 38:
            return f"{r}ª Rodada"

    except (ValueError, TypeError):
        pass

    return ROUND_NAMES.get(round_value, round_value)
