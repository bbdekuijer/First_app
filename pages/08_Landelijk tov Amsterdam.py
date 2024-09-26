import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Data voor stemmen per partij en per stadsdeel (Amsterdam 2021)
stadsdeel_data = pd.DataFrame({
    'Stadsdeel': ['Centrum', 'West', 'Zuid', 'Zuidoost', 'Oost', 'Noord', 'Nieuw-West'],
    'VVD': [6925, 7054, 19318, 3347, 7315, 4576, 6910],
    'D66': [15804, 17686, 26210, 4297, 18430, 7465, 9757],
    'PVV (Partij voor de Vrijheid)': [1789, 2232, 5667, 1866, 2128, 4492, 4006],
    'CDA': [1144, 1128, 4112, 732, 1243, 1028, 1428],
    'SP (Socialistische Partij)': [2481, 2876, 5387, 2226, 2897, 2725, 2886],
    'GroenLinks': [6210, 7142, 8137, 2176, 10090, 4377, 4982],
    'PvdA': [5100, 5356, 6017, 3255, 7080, 3086, 4150],
    'Total Votes': [56596, 67786, 106662, 33351, 70863, 45085, 60317]
})

# Landelijke stemmen Tweede Kamer 2021 (vervang door juiste data als beschikbaar)
landelijke_stemmen = pd.Series({
    'VVD': 2279145,
    'D66': 1565754,
    'PVV (Partij voor de Vrijheid)': 1124626,
    'CDA': 987134,
    'SP (Socialistische Partij)': 623371,
    'GroenLinks': 522411,
    'PvdA': 598690
})

# Functie om een barchart te maken die stadsdelen vergelijkt met het landelijke gemiddelde
def create_barchart(stadsdeel, row):
    partijen = ['VVD', 'D66', 'PVV (Partij voor de Vrijheid)', 'CDA', 'SP (Socialistische Partij)', 'GroenLinks', 'PvdA']
    stemmen_stadsdeel = [row[partij] for partij in partijen]
    
    # Bereken percentages per partij in het stadsdeel
    percentages_stadsdeel = [stemmen / row['Total Votes'] * 100 for stemmen in stemmen_stadsdeel]
    
    # Bereken landelijke percentages
    total_landelijk = landelijke_stemmen.sum()
    percentages_landelijk = [landelijke_stemmen[partij] / total_landelijk * 100 for partij in partijen]
    
    # Maak een dataframe voor de plot
    comparison_df = pd.DataFrame({
        'Partijen': partijen,
        'Amsterdam (Stadsdeel)': percentages_stadsdeel,
        'Nederland (Landelijk)': percentages_landelijk
    })

 # Plot de barchart
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.barplot(x='Partijen', y='value', hue='variable', 
                data=pd.melt(comparison_df, ['Partijen']), palette='Set2', ax=ax)
    plt.title(f"Vergelijking Stadsdeel {stadsdeel} vs. Landelijk")
    plt.ylabel('Percentage van stemmen (%)')
    plt.xticks(rotation=45)
    plt.tight_layout()
    st.pyplot(fig)

# Streamlit-app
st.title("Vergelijking van Amsterdamse Stadsdelen met Landelijk Gemiddelde (2021)")
st.write("Deze applicatie vergelijkt de stemmen per stadsdeel van Amsterdam met het landelijke gemiddelde van Nederland tijdens de Tweede Kamerverkiezingen van 2021.")

# Toon een checkbox voor elk stadsdeel en de grafiek alleen als deze aangevinkt is
for index, row in stadsdeel_data.iterrows():
    st.subheader(f"Stadsdeel: {row['Stadsdeel']}")
    
    # Checkbox toevoegen
    if st.checkbox(f"Toon diagram voor {row['Stadsdeel']}", key=row['Stadsdeel']):
        create_barchart(row['Stadsdeel'], row)
