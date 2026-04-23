from langdetect import detect, LangDetectException
import re


def find_tags(text):
    return re.findall(r"<[^>]+>", text)


def find_special_characters(text):
    return re.findall(r"[^\x00-\x7F]", text)


def detect_language(text):
    try:
        return detect(text)
    except LangDetectException:
        return "unknown"


def analyze_subtitles(subtitles):
    total = len(subtitles)
    all_tags = []
    special_chars = []
    full_text = ""

    for sub in subtitles:
        text = sub["text"]

        all_tags.extend(find_tags(text))
        special_chars.extend(find_special_characters(text))

        full_text += " " + text

    return {
        "total_subtitles": total,
        "unique_tags": list(set(all_tags)),
        "unique_special_characters": list(set(special_chars)),
        "overall_language": detect_language(full_text)
    }