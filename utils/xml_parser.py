import xml.etree.ElementTree as ET
import pandas as pd

def parse_surah_metadata(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    surahs = []
    for sura in root.find('suras'):
        surahs.append({
            'Surah': int(sura.get('index')),
            'Ayahs': int(sura.get('ayas')),
            'NameArabic': sura.get('name'),
            'NameTranslit': sura.get('tname'),
            'NameEnglish': sura.get('ename'),
            'Type': sura.get('type'),
            'Order': int(sura.get('order')),
            'Rukus': int(sura.get('rukus')),
        })

    return pd.DataFrame(surahs)