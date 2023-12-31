import transliterate


def cyrillic_to_latin(cyrillic_text: str) -> str:
    latin_text = transliterate.translit(value=cyrillic_text, language_code='ru', reversed=True)
    return latin_text


def pluralize(count: int, word: str) -> str:
    return word if count <= 1 else word + 's'
