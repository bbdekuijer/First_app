import streamlit as st
import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import numpy as np

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
st.title("Data Analyse van de Titanic Dataset")

# Introductie
st.write("In deze sectie kun je de dataset verkennen en de veranderingen zien die we hebben toegepast op de ontbrekende waarden.")

# Maak twee kolommen voor de data en de statistieken
col1, col2 = st.columns(2)

# Eerste kolom voor de eerste paar rijen van de dataset (voorafgaand aan bewerkingen)
with col1:
    st.subheader("Eerste 8 rijen van de dataset")
    st.dataframe(combined.head(8))

# Tweede kolom voor de basisstatistieken
with col2:
    st.subheader("Basisstatistieken van de dataset")
    st.write(combined.describe())  # Basisstatistieken van de dataset

# Aantal NaN-waarden in de dataset vóór de bewerkingen
nan_counts_before = combined.isnull().sum()
nan_data_before = pd.DataFrame({'Kolom': nan_counts_before.index, 'Aantal Missende Waarden': nan_counts_before.values})

# Vul de 'Age' kolom op met de mediaan per klasse
median_age_per_class = combined.groupby('Pclass')['Age'].median()
for pclass in median_age_per_class.index:
    combined.loc[(combined['Pclass'] == pclass) & (combined['Age'].isnull()), 'Age'] = median_age_per_class[pclass]

# Vul de 'Fare' kolom op met de mediaan van mensen met gelijke klasse en Embarked locatie
sim_fares = combined[(combined['Pclass'] == 3) & (combined['Embarked'] == 'S')]['Fare']
combined['Fare'].fillna(sim_fares.median(), inplace=True)

# Vul de 'Embarked' kolom op met 'C' voor de class 1 en Fare tussen 70 en 90
sim_emb = combined[(combined['Pclass'] == 1) & (combined['Fare'] >= 70) & (combined['Fare'] <= 90)]['Embarked']
combined['Embarked'].fillna('C', inplace=True)

# Vul de 'Cabin' kolom op met 'M' en trim naar de eerste letter
combined['Cabin'].fillna('M', inplace=True)
combined['Cabin'] = combined['Cabin'].str[0]

# Verander de 'T' in de 'Cabin' kolom naar 'M' (omdat het een typefout lijkt te zijn)
idx = np.where(combined['Cabin'] == 'T')[0]
combined.loc[idx, 'Cabin'] = 'M'

# Aantal NaN-waarden in de dataset na de bewerkingen
nan_counts_after = combined.isnull().sum()
nan_data_after = pd.DataFrame({'Kolom': nan_counts_after.index, 'Aantal Missende Waarden': nan_counts_after.values})

# Toon NaN count voor bewerkingen
st.subheader("Missende Waarden vóór de bewerkingen")
st.write(nan_data_before)

# Toon NaN count na bewerkingen
st.subheader("Missende Waarden na de bewerkingen")
st.write(nan_data_after)

# Extra uitleg
st.write("""
In deze sectie hebben we de volgende bewerkingen uitgevoerd op de dataset:
- **Leeftijd (`Age`)** is opgevuld met de mediaan per klasse.
- **Vervoersprijs (`Fare`)** is opgevuld met de mediaan van mensen met dezelfde klasse en embarcatie locatie.
- **Embark locatie (`Embarked`)** is opgevuld met de meest voorkomende locatie ('C') voor de juiste klasse en Fare-range.
- **Cabin** is opgevuld met 'M' en we hebben de letter 'T' aangepast naar 'M' vanwege vermoedelijke typefouten.
""")
