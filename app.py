# import streamlit as st
# from utils.quran_loader import load_quran
# from utils.text_cleaning import remove_diacritics
# from utils.xml_parser import parse_surah_metadata
# from visualizations.charts import plot_surah_occurrences
# from collections import Counter
# import re

# # --- Load Data ---
# quran_df = load_quran("data/quran-simple.txt", "data/en.ahmedali.txt")
# meta_df = parse_surah_metadata("data/quran-data.xml")
# df = quran_df.merge(meta_df, on='Surah', how='left')

# # --- UI ---
# st.title("📖 Quran Explorer")

# mode = st.radio("Choose a mode:", ["🔍 Search Word", "📖 Explore Surah"])

# # --- Word Search Mode ---
# if mode == "🔍 Search Word":
#     search_lang = st.radio("Choose the language to search in:", ["Arabic", "English"])

#     if search_lang == "Arabic":
#         search_term = st.text_input("Search for a word in the Quran (Arabic):")
#     else:
#         search_term = st.text_input("Search for a word in the Quran (English):")

#     context_n = st.selectbox("Number of surrounding words to show context (before/after):", list(range(1, 6)), index=1)

#     # --- Search Logic ---
#     if search_term:
#         if search_lang == "Arabic":
#             cleaned_search = remove_diacritics(search_term)
#             matches = df[df['TextClean'].str.contains(cleaned_search, case=False, na=False)]
#             context_col = 'TextClean'
#         else:
#             matches = df[df['TextEnglish'].str.contains(search_term, case=False, na=False)]
#             context_col = 'TextEnglish'

#         st.markdown(f"### 🔎 Found `{search_term}` in {len(matches)} verse(s).")
#         st.dataframe(matches[['Surah', 'Ayah', 'Text', 'TextEnglish', 'NameEnglish', 'Type']])

#         # --- Optional Surah Filtering (after search) ---
#         st.markdown("#### 📘 Optional: Filter by Surah")
#         unique_surahs = matches[['Surah', 'NameEnglish']].drop_duplicates().sort_values('Surah')
#         selected_surahs = st.multiselect(
#             "Select Surahs to filter results:",
#             options=unique_surahs['NameEnglish'],
#             default=unique_surahs['NameEnglish']
#         )

#         filtered_matches = matches[matches['NameEnglish'].isin(selected_surahs)]
#         st.markdown(f"Showing results from **{len(selected_surahs)}** Surah(s).")

#         # --- Surah-wise Aggregation ---
#         surah_count = filtered_matches.groupby(['Surah', 'NameEnglish', 'Type']).size().reset_index(name='Count')
#         st.markdown(f"### 📊 Surah-wise Occurrences of `{search_term}`:")
#         st.dataframe(surah_count)

#         # --- Chart ---
#         fig = plot_surah_occurrences(surah_count, search_term)
#         st.pyplot(fig)

#         # --- Contextual Analysis (Before/After Phrases) ---
#         st.markdown(f"### 🔁 Common {context_n}-word phrases before and after `{search_term}`")
#         before_phrases, after_phrases = [], []
#         for verse in filtered_matches[context_col].dropna():
#             words = re.findall(r'\b\w+\b', verse.lower())
#             for i, word in enumerate(words):
#                 if word == search_term.lower():
#                     before = words[max(0, i - context_n):i]
#                     after = words[i + 1:i + 1 + context_n]
#                     if len(before) == context_n:
#                         before_phrases.append(' '.join(before))
#                     if len(after) == context_n:
#                         after_phrases.append(' '.join(after))

#         before_counter = Counter(before_phrases).most_common(10)
#         after_counter = Counter(after_phrases).most_common(10)

#         st.markdown("#### ⬅️ Most common phrases *before* the word")
#         st.table(before_counter)

#         st.markdown("#### ➡️ Most common phrases *after* the word")
#         st.table(after_counter)

# # --- Surah Exploration Mode ---
# elif mode == "📖 Explore Surah":
#     st.markdown("### 📘 Select a Surah to Explore")

#     surah_names = df[['Surah', 'NameEnglish', 'NameArabic']].drop_duplicates()
#     display_names = surah_names['NameEnglish'] + " - " + surah_names['NameArabic']
#     selected = st.selectbox("Select a Surah:", display_names)

#     # Parse Surah ID
#     selected_surah = surah_names.iloc[display_names.tolist().index(selected)]['Surah']
#     surah_df = df[df['Surah'] == selected_surah]

#     # Metadata Display
#     st.markdown(f"### 📘 {selected}")
#     st.write("Verses:", len(surah_df))
#     st.write("Type:", surah_df['Type'].iloc[0])
#     st.write("Order:", surah_df['Order'].iloc[0])

#     # Language selection for word frequency
#     lang_choice = st.radio("Show word frequency in:", ["Arabic", "English"])

#     if lang_choice == "Arabic":
#         text_series = surah_df['TextClean']
#     else:
#         text_series = surah_df['TextEnglish']

#     # Word frequency logic
#     words = ' '.join(text_series.dropna()).lower()
#     words = re.findall(r'\b\w+\b', words)
#     word_counts = Counter(words)
#     common_words = word_counts.most_common(15)

#     # Show bar chart of most common words
#     st.markdown("### 🔠 Most Common Words")
#     st.bar_chart(dict(common_words))
import streamlit as st
from utils.quran_loader import load_quran
from utils.text_cleaning import remove_diacritics
from utils.xml_parser import parse_surah_metadata
from visualizations.charts import plot_surah_occurrences
from logic.search_logic import run_word_search
from logic.explore_logic import run_surah_explorer

# --- Load Data ---
quran_df = load_quran("data/quran-simple.txt", "data/en.ahmedali.txt")
meta_df = parse_surah_metadata("data/quran-data.xml")
df = quran_df.merge(meta_df, on='Surah', how='left')

# --- UI ---
st.title("📖 Quran Explorer")
mode = st.radio("Choose a mode:", ["🔍 Search Word", "📖 Explore Surah"])

if mode == "🔍 Search Word":
    run_word_search(df)
elif mode == "📖 Explore Surah":
    run_surah_explorer(df)
