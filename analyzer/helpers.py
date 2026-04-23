import re

def find_tags(text):
    return re.findall(r"<[^>]+>", text)

def find_special_characters(text):
    return re.findall(r"[^\x00-\x7F]", text)