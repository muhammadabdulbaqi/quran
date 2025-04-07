# import streamlit as st
# import matplotlib.pyplot as plt
# from utils.quran_loader import load_quran
# from utils.text_cleaning import remove_diacritics
# from utils.xml_parser import parse_surah_metadata

# # Load Quran data
# quran_df = load_quran("data/quran-simple.txt", "data/en.ahmedali.txt")
# meta_df = parse_surah_metadata("data/quran-data.xml")

# # Merge metadata
# df = quran_df.merge(meta_df, on='Surah', how='left')

# # --- UI ---
# st.title("🔍 Quran Word Search")

# search_lang = st.radio("Choose the language to search in:", ["Arabic", "English"])

# if search_lang == "Arabic":
#     search_term = st.text_input("Search for a word in the Quran (Arabic):")
# else:
#     search_term = st.text_input("Search for a word in the Quran (English):")

# if search_term:
#     if search_lang == "Arabic":
#         cleaned_search = remove_diacritics(search_term)
#         matches = df[df['TextClean'].str.contains(cleaned_search, case=False, na=False)]
#     else:
#         matches = df[df['TextEnglish'].str.contains(search_term, case=False, na=False)]

#     st.markdown(f"### 🔎 Found `{search_term}` in {len(matches)} verses.")
#     st.dataframe(matches[['Surah', 'Ayah', 'Text', 'TextEnglish', 'NameEnglish']])

#     surah_count = matches.groupby(['Surah', 'NameEnglish']).size().reset_index(name='Count')
#     st.markdown(f"### 📊 Surah-wise Occurrences of `{search_term}`:")
#     st.dataframe(surah_count)

#     fig, ax = plt.subplots(figsize=(10, 6))
#     ax.bar(surah_count['NameEnglish'], surah_count['Count'], color='lightgreen')
#     ax.set_xlabel("Surah")
#     ax.set_ylabel("Occurrences")
#     ax.set_title(f"Occurrences of '{search_term}' in Different Surahs")
#     ax.tick_params(axis='x', rotation=90)
#     st.pyplot(fig)

import streamlit as st
from utils.quran_loader import load_quran
from utils.text_cleaning import remove_diacritics
from utils.xml_parser import parse_surah_metadata
from visualizations.charts import plot_surah_occurrences

# --- Load Data ---
quran_df = load_quran("data/quran-simple.txt", "data/en.ahmedali.txt")
meta_df = parse_surah_metadata("data/quran-data.xml")
df = quran_df.merge(meta_df, on='Surah', how='left')

# --- UI ---
st.title("🔍 Quran Word Search")

search_lang = st.radio("Choose the language to search in:", ["Arabic", "English"])

if search_lang == "Arabic":
    search_term = st.text_input("Search for a word in the Quran (Arabic):")
else:
    search_term = st.text_input("Search for a word in the Quran (English):")

# --- Search Logic ---
if search_term:
    if search_lang == "Arabic":
        cleaned_search = remove_diacritics(search_term)
        matches = df[df['TextClean'].str.contains(cleaned_search, case=False, na=False)]
    else:
        matches = df[df['TextEnglish'].str.contains(search_term, case=False, na=False)]

    st.markdown(f"### 🔎 Found `{search_term}` in {len(matches)} verse(s).")
    st.dataframe(matches[['Surah', 'Ayah', 'Text', 'TextEnglish', 'NameEnglish', 'Type']])

    # --- Optional Surah Filtering (after search) ---
    st.markdown("#### 📘 Optional: Filter by Surah")
    unique_surahs = matches[['Surah', 'NameEnglish']].drop_duplicates().sort_values('Surah')
    selected_surahs = st.multiselect(
        "Select Surahs to filter results:",
        options=unique_surahs['NameEnglish'],
        default=unique_surahs['NameEnglish']
    )

    filtered_matches = matches[matches['NameEnglish'].isin(selected_surahs)]

    st.markdown(f"Showing results from **{len(selected_surahs)}** Surah(s).")

    # --- Surah-wise Aggregation ---
    surah_count = filtered_matches.groupby(['Surah', 'NameEnglish', 'Type']).size().reset_index(name='Count')
    
    st.markdown(f"### 📊 Surah-wise Occurrences of `{search_term}`:")
    st.dataframe(surah_count)

    # --- Chart ---
    fig = plot_surah_occurrences(surah_count, search_term)
    st.pyplot(fig)
