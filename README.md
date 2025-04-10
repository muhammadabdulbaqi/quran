# 📖 Quran Explorer

This is a Streamlit-based web application designed to explore the Quran in both Arabic and English. The app allows users to search for words/phrases in the Quran, filter results by Surah, view word frequency in a selected Surah, and generate visualizations for insights.

## Features

### 1. **Search Word Mode**
   - Users can search for a word or phrase in the Quran in either Arabic or English.
   - Results display the Surah, Ayah, and the verse text in the selected language.
   - Optional filtering allows users to narrow down results by selecting specific Surahs.
   - Surah-wise occurrence counts of the search term are shown, with a corresponding bar chart for visualization.

### 2. **Explore Surah Mode**
   - Users can select a specific Surah from a dropdown list.
   - Displays metadata about the selected Surah, including:
     - Number of verses
     - Surah type (Meccan/Medinan)
     - Surah order in the Quran
   - Users can choose to view the most common words in either Arabic or English within the Surah, visualized in a bar chart.

### Key Functions:

- **app.py**: Main script running the Streamlit app.
- **quran_loader.py**: Loads the Quran text data (both Arabic and English).
- **text_cleaning.py**: Contains functions for cleaning text (e.g., diacritic removal).
- **xml_parser.py**: Parses Surah metadata from an XML file and merges it with the Quran text data.
- **charts.py**: Contains visualization functions, including bar charts for Surah occurrences and word frequencies.

## Setup Instructions

1. **Clone the repository**:
git clone https://github.com/yourusername/quran-explorer.git cd quran-explorer

2. **Install required dependencies**:
Ensure you have Python 3.x installed, and then use `pip` to install required libraries.
pip install -r requirements.txt

3. **Download Quran Data**:
Ensure that the `data` folder contains the following files:
- `quran-simple.txt`: Arabic Quran text file.
- `en.ahmedali.txt`: English translation of the Quran.
- `quran-data.xml`: Surah metadata XML file.

4. **Run the app**:
To start the app, run:
streamlit run app.py


5. **Open the app**:
The app will be available in your browser at `http://localhost:8501`.

## Debugging

- **Common Issue**: When searching in Arabic, the word frequency chart may show individual letters rather than full words. This issue will be investigated in a later stage of development.

## Potential Next Steps

### 1. **Refining Word Frequency Logic**
- The current logic for extracting word frequencies in Arabic may need improvement to properly handle full words (instead of single letters).
- Debug and improve the word frequency extraction in Arabic text.

### 2. **Advanced Word Search Features**
- Allow users to search for multi-word phrases, not just single words.
- Improve the search mechanism to return more relevant results based on context, not just exact matches.

### 3. **Expand Surah Metadata**
- Enhance Surah metadata with additional details like the number of verses, historical context, and more.
- Add options to view additional metadata or insights based on Surah types (Meccan/Medinan).

### 4. **Surah Comparison**
- Implement a feature to compare different Surahs based on selected metrics (e.g., common word counts, verse lengths).
- Display a comparison chart to highlight differences.

### 5. **Word Cloud Visualization**
- Add a word cloud feature to visualize the most common words across all Surahs or within specific Surahs.

### 6. **Exporting Data**
- Allow users to export search results, word frequencies, or Surah metadata as CSV or JSON files for further analysis.

### 7. **User Feedback and Engagement**
- Add an option for users to rate the app or provide feedback directly in the interface.

### 8. **Deploy to Cloud**
- Host the app on platforms like Streamlit Cloud, Heroku, or AWS for public access.

---

## Contributions

Feel free to fork the repository and create pull requests if you would like to contribute to the project. Contributions are always welcome!

## License

This project is open-source and available under the MIT License. See the [LICENSE](LICENSE) file for more details.
