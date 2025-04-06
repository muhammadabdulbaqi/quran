import re

def remove_diacritics(text):
    text = re.sub(r'[\u064B-\u0652]', '', text)  # Harakat
    text = re.sub(r'\u0640', '', text)           # Tatwil
    text = text.replace('ٱ', 'ا')                # Alif with wasla
    return text