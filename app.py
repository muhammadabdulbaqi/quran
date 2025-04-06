# import streamlit as st
# import pandas as pd
# import re
# import matplotlib.pyplot as plt
# # import pyarabic.araby as araby

# # --- Diacritic removal function ---
# def remove_diacritics(text):
#     text = re.sub(r'[\u064B-\u0652]', '', text)  # Harakat
#     text = re.sub(r'\u0640', '', text)           # Tatwil
#     text = text.replace('ٱ', 'ا')                # Alif with wasla 

#     return text

# # --- Load and parse Quran ---
# @st.cache_data
# def load_quran(arabic_path, english_path=None):
#     parsed = []
    
#     # Read Arabic file
#     with open(arabic_path, 'r', encoding='utf-8') as f:
#         for line in f:
#             parts = line.strip().split('|', 2)
#             if len(parts) != 3:
#                 continue
#             surah, ayah, text = parts
#             parsed.append((int(surah), int(ayah), text))
    
#     # Create initial DataFrame
#     df = pd.DataFrame(parsed, columns=['Surah', 'Ayah', 'Text'])
#     df['TextClean'] = df['Text'].apply(remove_diacritics)
    
#     if english_path:
#         english_lines = []
#         with open(english_path, 'r', encoding='utf-8') as ef:
#             for line in ef:
#                 parts = line.strip().split('|', 2)
#                 if len(parts) != 3:
#                     # english_lines.append("")  # To maintain alignment
#                     continue
#                 _, _, text = parts
#                 english_lines.append(text)

#         # Add English text as new column
#         if len(english_lines) == len(df):
#             df['TextEnglish'] = english_lines
#         else:
#             raise ValueError("Mismatch between Arabic and English verse count.")
    
#     return df


# df = load_quran("quran-simple.txt", "en.ahmedali.txt")

# # --- Title ---
# st.title("🔍 Quran Word Search")

# # --- Language Selection ---
# search_lang = st.radio("Choose the language to search in:", ["Arabic", "English"])

# # --- Search Input ---
# if search_lang == "Arabic":
#     search_term = st.text_input("Search for a word in the Quran (Arabic):")
# else:
#     search_term = st.text_input("Search for a word in the Quran (English):")

# # --- Search Logic ---
# if search_term:
#     if search_lang == "Arabic":
#         cleaned_search = remove_diacritics(search_term)
#         matches = df[df['TextClean'].str.contains(cleaned_search, case=False, na=False)]
#     else:
#         matches = df[df['TextEnglish'].str.contains(search_term, case=False, na=False)]

#     st.markdown(f"### 🔎 Found `{search_term}` in {len(matches)} verses.")

#     # --- Display Matching Verses ---
#     st.markdown("### 📖 Matching Verses:")
#     st.dataframe(matches[['Surah', 'Ayah', 'Text', 'TextEnglish']])

#     # --- Surah-wise Visualization ---
#     surah_count = matches.groupby('Surah').size().reset_index(name='Count')

#     st.markdown(f"### 📊 Surah-wise Occurrences of `{search_term}`:")
#     st.dataframe(surah_count)

#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.bar(surah_count['Surah'].astype(str), surah_count['Count'], color='lightgreen')
#     ax.set_xlabel("Surah")
#     ax.set_ylabel("Occurrences")
#     ax.set_title(f"Occurrences of '{search_term}' in Different Surahs")
#     st.pyplot(fig)

import streamlit as st
import matplotlib.pyplot as plt
from utils.quran_loader import load_quran
from utils.text_cleaning import remove_diacritics
from utils.xml_parser import parse_surah_metadata

# Load Quran data
quran_df = load_quran("data/quran-simple.txt", "data/en.ahmedali.txt")
meta_df = parse_surah_metadata("data/quran-data.xml")

# Merge metadata
df = quran_df.merge(meta_df, on='Surah', how='left')

# --- UI ---
st.title("🔍 Quran Word Search")

search_lang = st.radio("Choose the language to search in:", ["Arabic", "English"])

if search_lang == "Arabic":
    search_term = st.text_input("Search for a word in the Quran (Arabic):")
else:
    search_term = st.text_input("Search for a word in the Quran (English):")

if search_term:
    if search_lang == "Arabic":
        cleaned_search = remove_diacritics(search_term)
        matches = df[df['TextClean'].str.contains(cleaned_search, case=False, na=False)]
    else:
        matches = df[df['TextEnglish'].str.contains(search_term, case=False, na=False)]

    st.markdown(f"### 🔎 Found `{search_term}` in {len(matches)} verses.")
    st.dataframe(matches[['Surah', 'Ayah', 'Text', 'TextEnglish', 'NameEnglish']])

    surah_count = matches.groupby(['Surah', 'NameEnglish']).size().reset_index(name='Count')
    st.markdown(f"### 📊 Surah-wise Occurrences of `{search_term}`:")
    st.dataframe(surah_count)

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.bar(surah_count['NameEnglish'], surah_count['Count'], color='lightgreen')
    ax.set_xlabel("Surah")
    ax.set_ylabel("Occurrences")
    ax.set_title(f"Occurrences of '{search_term}' in Different Surahs")
    ax.tick_params(axis='x', rotation=90)
    st.pyplot(fig)