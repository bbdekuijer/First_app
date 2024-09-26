import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from io import BytesIO

# Data voor stemmen per partij en per stadsdeel
stadsdeel_data = pd.DataFrame({
    'Stadsdeel': ['Centrum', 'West', 'Zuid', 'Zuidoost', 'Oost', 'Noord', 'Nieuw-West'],
    'VVD': [6925, 7054, 19318, 3347, 7315, 4576, 6910],
    'D66': [15804, 17686, 26210, 4297, 18430, 7465, 9757],
    'PVV': [1789, 2232, 5667, 1866, 2128, 4492, 4006],  # Tussen haakjes verwijderd
    'CDA': [1144, 1128, 4112, 732, 1243, 1028, 1428],
    'SP': [2481, 2876, 5387, 2226, 2897, 2725, 2886],  # Tussen haakjes verwijderd
    'GroenLinks': [6210, 7142, 8137, 2176, 10090, 4377, 4982],
    'PvdA': [5100, 5356, 6017, 3255, 7080, 3086, 4150],
    'Total Votes': [56596, 67786, 106662, 33351, 70863, 45085, 60317]
})

# Partijen kolommen zonder tussen haakjes
partij_columns = ['VVD', 'D66', 'PVV', 'CDA', 'SP', 'GroenLinks', 'PvdA']

# Bereken percentages per partij voor Nieuw-West
nieuw_west_row = stadsdeel_data[stadsdeel_data['Stadsdeel'] == 'Nieuw-West'].iloc[0]
for partij in partij_columns:
    stadsdeel_data.loc[stadsdeel_data['Stadsdeel'] == 'Nieuw-West', partij + ' %'] = (nieuw_west_row[partij] / nieuw_west_row['Total Votes']) * 100

# Functie om taartdiagrammen te maken voor Nieuw-West
def create_pie_chart(row, stadsdeel):
    labels = partij_columns
    sizes = [row[partij] for partij in partij_columns]
    
    # Gebruik een Seaborn palet voor consistente kleuren
    colors = sns.color_palette("Set2", len(partij_columns))
    
    # Maak het taartdiagram
    fig, ax = plt.subplots()
    ax.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
    ax.axis('equal')  # Zorg dat de taart een cirkel is
    plt.title(f"Stemverdeling in {stadsdeel}")
    
    # Sla de grafiek op als PNG in geheugen
    img_bytes = BytesIO()
    plt.savefig(img_bytes, format='png', bbox_inches='tight')
    plt.close(fig)  # Sluit de figuur
    img_bytes.seek(0)
    
    return img_bytes

# Hoofd Streamlit-app
st.title("Stemverdeling per Stadsdeel in Amsterdam")

# Genereer een taartdiagram voor Nieuw-West en toon het
img_bytes = create_pie_chart(nieuw_west_row, nieuw_west_row['Stadsdeel'])
st.image(img_bytes, caption=f"Stemverdeling in {nieuw_west_row['Stadsdeel']}", use_column_width=True)

