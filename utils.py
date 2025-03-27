import unicodedata


def normalize_text(text: str) -> str:
    normalized_text = unicodedata.normalize('NFD', text)
    # Remove diacritics and convert to lowercase
    return ''.join(c for c in normalized_text if unicodedata.category(c) != 'Mn').lower()
