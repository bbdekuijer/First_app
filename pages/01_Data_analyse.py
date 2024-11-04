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

# Sectie voor NaN-verdeling met staafdiagram
st.subheader("Verdeling van Missende Waarden per Kolom")
# Maak een dataframe dat telt hoeveel NaN's er in elke kolom zitten
nan_data = pd.DataFrame(data.isna().sum(), columns=['NaN Count']).reset_index()
nan_data.columns = ['Column', 'NaN Count']

# Maak een staafdiagram voor de NaN-waarden
fig_nan_bar = px.bar(nan_data, x='Column', y='NaN Count', title="Aantal Missende Waarden per Kolom")
fig_nan_bar.update_layout(
    xaxis_title="Kolommen",
    yaxis_title="Aantal Missende Waarden",
    showlegend=False
)
st.plotly_chart(fig_nan_bar)

# Titel voor leeftijdsdistributie en passagiersklasse-selectiebox
st.subheader("Leeftijdsdistributie per Passagiersklasse")
pclass_options = sorted(data['Pclass'].unique())
pclass = st.selectbox("Selecteer een passagiersklasse:", pclass_options)

# Filter de data op basis van de geselecteerde klasse en verwijder NaN-waarden in de Age kolom
filtered_data = data[(data['Pclass'] == pclass) & (data['Age'].notna())]

# Maak de histogram met vaste x-as limieten, bin-grootte en kleuren
fig_age_dist = px.histogram(
    filtered_data,
    x='Age',
    title=f"Leeftijdsdistributie voor Passagiers in Klasse {pclass}",
    labels={'Age': 'Leeftijd'},
    color='Survived',
    color_discrete_sequence=['#FFA07A', '#90EE90'],  # Kleuren: zacht oranje en lichtgroen
    category_orders={'Survived': [0, 1]}
)

# Forceer de bin-grootte op 5 (zodat 80/5 = 16 bins) en stel de x-as vast van 0 tot 80
fig_age_dist.update_traces(xbins=dict(start=0, end=80, size=5))
fig_age_dist.update_layout(
    legend_title_text='Overleving',
    xaxis_title='Leeftijd',
    yaxis_title='Aantal Passagiers',
    xaxis=dict(range=[0, 80])  # Stel de x-as limiet vast van 0 tot 80
)

# Weergave van de grafiek
st.plotly_chart(fig_age_dist)
