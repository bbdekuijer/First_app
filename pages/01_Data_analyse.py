import streamlit as st
import pandas as pd
import plotly.express as px

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Hoofdtitel
st.title("Data Analyse")

# Introductie
st.write("In deze sectie kun je de dataset verkennen en basisstatistieken bekijken.")

# Maak twee kolommen voor de data en de statistieken
col1, col2 = st.columns(2)

# Eerste kolom voor de eerste paar rijen van de dataset
with col1:
    st.subheader("Gegevens")
    st.dataframe(data.head(8))  # Laat de eerste 8 rijen van de dataset zien

# Tweede kolom voor de basisstatistieken
with col2:
    st.subheader("Basis Statistieken")
    st.write(data.describe())  # Basisstatistieken van de dataset

# Zet de klassen in de juiste volgorde
pclass_options = sorted(data['Pclass'].unique())

# Titel voor leeftijdsdistributie en passagiersklasse-selectiebox
st.subheader("Leeftijdsdistributie per Passagiersklasse")
pclass = st.selectbox("Selecteer een passagiersklasse:", pclass_options)

# Filter de data op basis van de geselecteerde klasse en verwijder NaN-waarden in de Age kolom
filtered_data = data[(data['Pclass'] == pclass) & (data['Age'].notna())]

# Maak de histogram met aangepaste kleuren en vaste x-as limieten
fig_age_dist = px.histogram(
    filtered_data,
    x='Age',
    nbins=30,
    title=f"Leeftijdsdistributie voor Passagiers in Klasse {pclass}",
    labels={'Age': 'Leeftijd'},
    color='Survived',
    color_discrete_map={0: 'lightblue', 1: 'lightgreen'},
    category_orders={'Survived': [0, 1]}
)

# Voeg een legenda toe en stel de x-as limiet vast
fig_age_dist.update_layout(
    legend_title_text='Overleving',
    xaxis_title='Leeftijd',
    yaxis_title='Aantal Passagiers',
    xaxis=dict(range=[0, 80])  # Stel de x-as limiet van 0 tot 80
)

# Weergave van de grafiek
st.plotly_chart(fig_age_dist)
