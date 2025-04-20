import streamlit as st
from collections import Counter
import re
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import plotly.express as px
from itertools import islice, tee

def get_ngrams(words, n):
    return zip(*(islice(seq, i, None) for i, seq in enumerate(tee(words, n))))

def run_quran_insights(df):
    st.header("📊 Quran Insights")

    # --- Word Cloud (English only) ---
    st.subheader("☁️ Most Frequent Words (English Only)")
    eng_words = ' '.join(df['TextEnglish'].dropna()).lower()
    eng_word_list = re.findall(r'\b\w+\b', eng_words)
    word_freq = Counter(eng_word_list)

    wc = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(word_freq)
    fig_wc, ax_wc = plt.subplots(figsize=(10, 5))
    ax_wc.imshow(wc, interpolation='bilinear')
    ax_wc.axis('off')
    st.pyplot(fig_wc)

    # --- Bigram/Trigram Toggle ---
    st.subheader("📘 Frequent Phrases")
    lang_choice = st.radio("Choose language for bigram/trigram analysis:", ["Arabic", "English"])

    if lang_choice == "Arabic":
        text_series = df['TextClean']
    else:
        text_series = df['TextEnglish']

    full_text = ' '.join(text_series.dropna()).lower()
    word_list = re.findall(r'\b\w+\b', full_text)

    # Bigrams
    bigrams = Counter([' '.join(b) for b in get_ngrams(word_list, 2)])
    st.markdown("#### 🔁 Most Common Bigrams")
    st.table(bigrams.most_common(15))

    # Trigrams
    trigrams = Counter([' '.join(t) for t in get_ngrams(word_list, 3)])
    st.markdown("#### 🔁 Most Common Trigrams")
    st.table(trigrams.most_common(15))

    # --- Interactive Revelation Timeline ---
    st.subheader("📜 Chronological Revelation Timeline")

    unique_surahs = df.drop_duplicates(subset='Surah')[['Surah', 'NameEnglish', 'Order', 'Type']].sort_values(by='Order')
    fig_timeline = px.scatter(
        unique_surahs,
        x="Order",
        y=[0]*len(unique_surahs),  # dummy Y axis
        color="Type",
        color_discrete_map={"Meccan": "blue", "Medinan": "green"},
        hover_name="NameEnglish",
        labels={"Order": "Revelation Order"},
        title="Surahs in Order of Revelation (Hover to View Names)",
    )
    fig_timeline.update_yaxes(visible=False)
    fig_timeline.update_layout(height=250, showlegend=True)
    st.plotly_chart(fig_timeline, use_container_width=True)
