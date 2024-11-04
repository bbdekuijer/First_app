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

# Selectiebox voor passagiersklasse
pclass = st.selectbox("Selecteer een passagiersklasse:", data['Pclass'].unique())

# Bereken de gemiddelde leeftijd per passagiersklasse
avg_age = data[data['Pclass'] == pclass]['Age'].mean()

# Toon gemiddelde leeftijd
st.write(f"De gemiddelde leeftijd voor passagiers in klasse {pclass} is {avg_age:.2f} jaar.")

# Creëer een DataFrame voor de visualisatie van gemiddelde leeftijden
age_data = data.groupby('Pclass')['Age'].mean().reset_index()

# Interactieve grafiek van de gemiddelde leeftijd per passagiersklasse
fig_age = px.bar(age_data, x='Pclass', y='Age', 
                  title="Gemiddelde Leeftijd per Passagiersklasse",
                  labels={'Pclass': 'Passagiersklasse', 'Age': 'Gemiddelde Leeftijd'},
                  color='Age', color_continuous_scale=px.colors.sequential.Plasma)

# Voeg een lijn toe voor de gemiddelde leeftijd van de geselecteerde klasse
fig_age.add_scatter(x=[pclass], y=[avg_age], mode='markers+text', 
                    marker=dict(color='red', size=10),
                    text=["Gemiddelde Leeftijd geselecteerde klasse"],
                    textposition="top center")

# Weergave van de grafiek
st.plotly_chart(fig_age)
