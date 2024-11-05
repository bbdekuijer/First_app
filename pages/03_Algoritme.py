import streamlit as st
import pandas as pd
import numpy as np

# Laad de dataset
data_path = "Data/Raw/train.csv"  # Pas dit pad aan naar de juiste locatie van je data
data = pd.read_csv(data_path)

# Hoofdtitel
st.title("Data Voorbereiding - Titanic Case")

# Introductie
st.write("Deze pagina toont stap voor stap de voorbereidingen die zijn uitgevoerd op de Titanic dataset voor verdere analyse en modelontwikkeling.")

### Stap 1: Missing Values
st.subheader("Stap 1: Verwijderen van Kolommen met Veel Missende Waarden")
st.write("Bepaalde kolommen bevatten veel ontbrekende waarden. Deze kolommen verwijderen we, omdat ze weinig bruikbare informatie toevoegen.")

# Bekijk de missende waarden per kolom
missing_values = data.isna().sum()
st.write("Aantal missende waarden per kolom:")
st.dataframe(missing_values)

# Specificeer de kolommen die verwijderd worden en pas dit toe
cols_to_drop = ['Cabin', 'Ticket']  # Bijvoorbeeld Cabin en Ticket
data_cleaned = data.drop(columns=cols_to_drop)
st.write(f"De volgende kolommen zijn verwijderd: {', '.join(cols_to_drop)}")
st.dataframe(data_cleaned.head())

### Stap 2: Omzetten van Embarked naar Volledige Namen
st.subheader("Stap 2: Omzetten van 'Embarked' Codes naar Volledige Namen")
st.write("We vervangen de afkortingen van de kolom 'Embarked' door de volledige plaatsnamen voor meer leesbaarheid.")

# Vervang de codes in de Embarked kolom
data_cleaned['Embarked'] = data_cleaned['Embarked'].map({'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'})
st.write("Na deze stap zijn de codes in de kolom 'Embarked' vervangen door volledige plaatsnamen.")
st.dataframe(data_cleaned[['Embarked']].head())

### Stap 3: Missende Waarden Invullen
st.subheader("Stap 3: Invullen van Missende Waarden")
st.write("We vullen de missende waarden in de kolommen 'Age' en 'Embarked' in met relevante statistische waarden, gebaseerd op passagiersklasse.")

# Vul missende Embarked waarden in met de meest voorkomende locatie
data_cleaned['Embarked'].fillna('Southampton', inplace=True)
st.write("Missende waarden in de kolom 'Embarked' zijn ingevuld met de meest voorkomende haven: Southampton.")

# Vul missende waarden in de kolom 'Age' op basis van de gemiddelde leeftijd per klasse
data_cleaned['Age'] = data_cleaned.groupby('Pclass')['Age'].transform(lambda x: x.fillna(x.median()))
st.write("Missende waarden in de kolom 'Age' zijn ingevuld met de mediaanleeftijd per passagiersklasse.")
st.dataframe(data_cleaned[['Age', 'Pclass']].head(10))

### Stap 4: Converteer Categorieën naar Numerieke Waarden
st.subheader("Stap 4: Omzetten van Categorieën naar Numerieke Waarden")
st.write("Om de dataset geschikt te maken voor machine learning, zetten we bepaalde categorische kolommen om naar numerieke waardes.")

# Converteer 'Sex' naar numerieke waarden
data_cleaned['Sex'] = data_cleaned['Sex'].map({'male': 0, 'female': 1})
st.write("De kolom 'Sex' is omgezet naar numerieke waarden (0 voor man, 1 voor vrouw).")
st.dataframe(data_cleaned[['Sex']].head())

# Toon het eindresultaat
st.subheader("Geëindigde Dataset na Verwerking")
st.write("Hier is de dataset na het uitvoeren van alle dataverwerkingsstappen:")
st.dataframe(data_cleaned.head(10))

# Opslaan als CSV-bestand (optioneel, als je de aangepaste data wilt opslaan)
save_path = "Data/Processed/train_cleaned.csv"  # Pas dit pad aan zoals gewenst
data_cleaned.to_csv(save_path, index=False)
st.write(f"De verwerkte dataset is opgeslagen als `{save_path}`.")
