import unicodedata

def normalize(text: str) -> str:

    text = text.lower().strip()

    return ''.join(
        c for c in unicodedata.normalize('NFD', text)
        if unicodedata.category(c) != 'Mn'
    )