import transliterate


def cyrillic_to_latin(cyrillic_text: str) -> str:
    """
    Translates Cyrillic text to Latin text.

    Args:
        cyrillic_text (str): The text in Cyrillic to be translated.

    Returns:
        str: The translated text in Latin.

    """
    latin_text = transliterate.translit(value=cyrillic_text, language_code='ru', reversed=True)
    return latin_text


def pluralize(count: int, word: str) -> str:
    """
    Return the plural form of a word based on the count.

    Parameters:
    count (int): The count of the objects.
    word (str): The word to be pluralized.

    Returns:
    str: The plural form of the word if the count is greater than 1, otherwise the original word.

    Example:
    >>> pluralize(1, 'apple')
    'apple'
    >>> pluralize(2, 'apple')
    'apples'
    """
    return word if count <= 1 else word + 's'
