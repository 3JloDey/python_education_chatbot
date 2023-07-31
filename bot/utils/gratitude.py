import re
from difflib import SequenceMatcher


def gratitude_checker(text: str | None, coefficient: float | int = 0.85) -> bool:
    gratitude_keywords = ("спасибо", "спасибки", "спс", "благодарю", "мерси")

    if text is not None:
        for word in text.lower().split():
            clean_word = re.sub("[^a-zA-Zа-яА-Я]", "", word)

            for keyword in gratitude_keywords:
                similarity_ratio = SequenceMatcher(None, clean_word, keyword).ratio()
                if similarity_ratio >= coefficient or keyword in clean_word:
                    return True
    return False
