import streamlit as st
import re
from collections import Counter

def run_surah_explorer(df):
    st.markdown("### 📘 Select a Surah to Explore")
    surah_names = df[['Surah', 'NameEnglish', 'NameArabic']].drop_duplicates()
    display_names = surah_names['NameEnglish'] + " - " + surah_names['NameArabic']
    selected = st.selectbox("Select a Surah:", display_names)

    selected_surah = surah_names.iloc[display_names.tolist().index(selected)]['Surah']
    surah_df = df[df['Surah'] == selected_surah]

    st.markdown(f"### 📘 {selected}")
    st.write("Verses:", len(surah_df))
    st.write("Type:", surah_df['Type'].iloc[0])
    st.write("Order:", surah_df['Order'].iloc[0])

    lang_choice = st.radio("Show word frequency in:", ["Arabic", "English"])
    remove_stops = st.checkbox("Remove stop words")

    if lang_choice == "Arabic":
        text_series = surah_df['TextClean']
        stop_words = set()
        if remove_stops:
            with open("data/stop_ar.txt", encoding="utf-8") as f:
                stop_words = set(line.strip() for line in f if line.strip())
    else:
        text_series = surah_df['TextEnglish']
        stop_words = set()
        if remove_stops:
            with open("data/stop_eng.txt", encoding="utf-8") as f:
                stop_words = set(line.strip().lower() for line in f if line.strip())

    words = ' '.join(text_series.dropna()).lower()
    words = re.findall(r'\b\w+\b', words)
    if remove_stops:
        words = [word for word in words if word not in stop_words]

    word_counts = Counter(words)
    common_words = word_counts.most_common(15)

    st.markdown("### 🔠 Most Common Words")
    st.bar_chart(dict(common_words))
