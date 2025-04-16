import streamlit as st
from collections import Counter
import re
from utils.text_cleaning import remove_diacritics
from visualizations.charts import plot_surah_occurrences

def run_word_search(df):
    search_lang = st.radio("Choose the language to search in:", ["Arabic", "English"])

    if search_lang == "Arabic":
        search_term = st.text_input("Search for a word in the Quran (Arabic):")
    else:
        search_term = st.text_input("Search for a word in the Quran (English):")

    context_n = st.selectbox("Number of surrounding words to show context (before/after):", list(range(1, 6)), index=1)

    if search_term:
        if search_lang == "Arabic":
            cleaned_search = remove_diacritics(search_term)
            matches = df[df['TextClean'].str.contains(cleaned_search, case=False, na=False)]
            context_col = 'TextClean'
        else:
            matches = df[df['TextEnglish'].str.contains(search_term, case=False, na=False)]
            context_col = 'TextEnglish'

        st.markdown(f"### 🔎 Found `{search_term}` in {len(matches)} verse(s).")
        st.dataframe(matches[['Surah', 'Ayah', 'Text', 'TextEnglish', 'NameEnglish', 'Type']])

        unique_surahs = matches[['Surah', 'NameEnglish']].drop_duplicates().sort_values('Surah')
        selected_surahs = st.multiselect(
            "Select Surahs to filter results:",
            options=unique_surahs['NameEnglish'],
            default=unique_surahs['NameEnglish']
        )

        filtered_matches = matches[matches['NameEnglish'].isin(selected_surahs)]
        st.markdown(f"Showing results from **{len(selected_surahs)}** Surah(s).")

        surah_count = filtered_matches.groupby(['Surah', 'NameEnglish', 'Type']).size().reset_index(name='Count')
        st.markdown(f"### 📊 Surah-wise Occurrences of `{search_term}`:")
        st.dataframe(surah_count)

        fig = plot_surah_occurrences(surah_count, search_term)
        st.pyplot(fig)

        # Contextual analysis: most frequent N-word sequences before and after the search term
        st.markdown(f"### 🔁 Common {context_n}-word phrases before and after `{search_term}`")
        before_phrases, after_phrases = [], []
        for verse in filtered_matches[context_col].dropna():
            words = re.findall(r'\b\w+\b', verse.lower())
            for i, word in enumerate(words):
                if word == search_term.lower():
                    before = words[max(0, i - context_n):i]
                    after = words[i + 1:i + 1 + context_n]
                    if len(before) == context_n:
                        before_phrases.append(' '.join(before))
                    if len(after) == context_n:
                        after_phrases.append(' '.join(after))

        before_counter = Counter(before_phrases).most_common(10)
        after_counter = Counter(after_phrases).most_common(10)

        st.markdown("#### ⬅️ Most common phrases *before* the word")
        st.table(before_counter)

        st.markdown("#### ➡️ Most common phrases *after* the word")
        st.table(after_counter)
