import streamlit as st
import pandas as pd
import plotly.express as px

# Laad de dataset
train = pd.read_csv('Data/Raw/train.csv')
test = pd.read_csv('Data/Raw/test.csv')

# Training dataset heeft een 'survived' kolom. We slaan dit op als een variabele. 
survived = train['Survived']

# We verwijderen de 'survived' kolom uit de train dataset. 
train = train.drop(['Survived'], axis=1)

# We extraheren de passagiers-ID's uit beide datasets. 
train_ID = train['PassengerId']
test_ID = test['PassengerId']

# Hier combineren we de ID's van de twee datasets en maken we de index schoon. 
combined = pd.concat([train, test]).reset_index(drop=True)

# Hoofdtitel
st.title("Data Analyse")

# Introductie
st.write("In deze sectie kun je de dataset verkennen en basisstatistieken bekijken.")

# Maak twee kolommen voor de data en de statistieken
col1, col2 = st.columns(2)

# Eerste kolom voor de eerste paar rijen van de dataset
with col1:
    st.subheader("Gegevens")
    st.dataframe(combined.head(8))  # Laat de eerste 8 rijen van de dataset zien

# Tweede kolom voor de basisstatistieken
with col2:
    st.subheader("Basis Statistieken")
    st.write(combined.describe())  # Basisstatistieken van de dataset

# Aantal NaN-waarden in elke kolom
nan_counts = combined.isnull().sum()
nan_data = pd.DataFrame({'Column': nan_counts.index, 'NaN Count': nan_counts.values})

# Display NaN count als een tabel
st.subheader("Aantal Missende Waarden per Kolom")
st.write(nan_data)

# Vul de 'Age' kolom op met de mediaan per klasse
median_age_per_class = combined.groupby('Pclass')['Age'].median()
for pclass in median_age_per_class.index:
    combined.loc[(combined['Pclass'] == pclass) & (combined['Age'].isnull()), 'Age'] = median_age_per_class[pclass]

# Controleer op missende waarden na het invullen
nan_counts_after = combined.isnull().sum()
nan_data_after = pd.DataFrame({'Column': nan_counts_after.index, 'NaN Count': nan_counts_after.values})

# Toon de bijgewerkte NaN-telling
st.subheader("Aantal Missende Waarden na Het Opvullen van de Leeftijd")
st.write(nan_data_after)

# Weergave van de eerste paar rijen na het invullen
st.subheader("Gegevens na het Opvullen van de Leeftijd")
st.dataframe(combined.head(8))
