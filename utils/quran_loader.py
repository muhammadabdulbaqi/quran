import pandas as pd
from .text_cleaning import remove_diacritics

def load_quran(arabic_path, english_path=None):
    parsed = []
    with open(arabic_path, 'r', encoding='utf-8') as f:
        for line in f:
            parts = line.strip().split('|', 2)
            if len(parts) != 3:
                continue
            surah, ayah, text = parts
            parsed.append((int(surah), int(ayah), text))

    df = pd.DataFrame(parsed, columns=['Surah', 'Ayah', 'Text'])
    df['TextClean'] = df['Text'].apply(remove_diacritics)

    if english_path:
        english_lines = []
        with open(english_path, 'r', encoding='utf-8') as ef:
            for line in ef:
                parts = line.strip().split('|', 2)
                if len(parts) != 3:
                    continue
                _, _, text = parts
                english_lines.append(text)

        if len(english_lines) == len(df):
            df['TextEnglish'] = english_lines
        else:
            raise ValueError("Mismatch between Arabic and English verse count.")

    return df