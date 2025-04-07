import matplotlib.pyplot as plt

def plot_surah_occurrences(df, word):
    fig, ax = plt.subplots(figsize=(10, 6))

    type_to_color = {
        'Meccan': 'skyblue',
        'Medinan': 'lightgreen'
    }

    # Map colors based on 'Type'
    colors = df['Type'].map(type_to_color)

    ax.bar(df['NameEnglish'], df['Count'], color=colors)
    ax.set_xlabel("Surah")
    ax.set_ylabel("Occurrences")
    ax.set_title(f"Occurrences of '{word}' in Different Surahs")
    ax.tick_params(axis='x', rotation=90)

    # Create legend
    handles = [plt.Rectangle((0, 0), 1, 1, color=color) for color in type_to_color.values()]
    labels = list(type_to_color.keys())
    ax.legend(handles, labels, title="Surah Type")

    return fig
