import streamlit as st
from utils.quran_loader import load_quran
from utils.text_cleaning import remove_diacritics
from utils.xml_parser import parse_surah_metadata
from visualizations.charts import plot_surah_occurrences
from logic.search_logic import run_word_search
from logic.explore_logic import run_surah_explorer
from logic.insights_logic import run_quran_insights  # NEW

# --- Load Data ---
quran_df = load_quran("data/quran-simple.txt", "data/en.ahmedali.txt")
meta_df = parse_surah_metadata("data/quran-data.xml")
df = quran_df.merge(meta_df, on='Surah', how='left')

# --- UI ---
st.title("📖 Quran Explorer")
mode = st.radio("Choose a mode:", ["🔍 Search Word", "📖 Explore Surah", "📊 Quran Insights"])

if mode == "🔍 Search Word":
    run_word_search(df)
elif mode == "📖 Explore Surah":
    run_surah_explorer(df)
elif mode == "📊 Quran Insights":
    run_quran_insights(df)
