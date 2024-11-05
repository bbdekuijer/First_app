import streamlit as st
import pandas as pd
import numpy as np

# Laad de dataset
train = pd.read_csv('Data/Raw/train.csv')
test = pd.read_csv('Data/Raw/test.csv')

# Training dataset heeft een 'Survived' kolom. We slaan dit op als een variabele.
survived = train['Survived']
train = train.drop(['Survived'], axis=1)

# Combineer de data en reset de index
combined = pd.concat([train, test]).reset_index(drop=True)

# Hoofdtitel
st.title("Titanic Data voor Machine Learning")

# Introductie
st.write("""
In deze analyse bewerken we de Titanic-dataset, zodat deze geschikt wordt voor het trainen van een Random Forest-model. 
We leggen uit welke bewerkingen we uitvoeren en waarom deze nodig zijn voor betere prestaties.
""")

# Toon de eerste paar rijen van de originele dataset
st.subheader("Originele Data")
st.write(combined.head(8))

# 1. Missende Waarden in Leeftijd en andere kolommen
st.subheader("Stap 1: Opvullen van Missende Waarden")

# Aantal NaN-waarden vóór de bewerkingen
nan_counts_before = combined.isnull().sum()
st.write("Aantal missende waarden per kolom vóór de bewerkingen:")
st.write(nan_counts_before[nan_counts_before > 0])

# Extra uitleg
st.write("""
In deze sectie hebben we de volgende bewerkingen uitgevoerd op de dataset:
- **Leeftijd (Age)** is opgevuld met de mediaan per klasse.
- **Vervoersprijs (Fare)** is opgevuld met de mediaan van mensen met dezelfde klasse en embarcatie locatie.
- **Cabin** is opgevuld met 'M' en we hebben de letter 'T' aangepast naar 'M' vanwege vermoedelijke typefouten.
- **Embark locatie (Embarked)** is opgevuld met de meest voorkomende locatie ('C') voor de juiste klasse en Fare-range.
""")

# Vul 'Age' met mediane leeftijd per klasse
median_age_per_class = combined.groupby('Pclass')['Age'].median()
for pclass in median_age_per_class.index:
    combined.loc[(combined['Pclass'] == pclass) & (combined['Age'].isnull()), 'Age'] = median_age_per_class[pclass]

# Vul 'Fare' met mediaan van dezelfde klasse en Embarked-locatie
sim_fares = combined[(combined['Pclass'] == 3) & (combined['Embarked'] == 'S')]['Fare']
combined['Fare'].fillna(sim_fares.median(), inplace=True)

# Vul 'Embarked' op met de meest voorkomende waarde 'C' voor specifieke voorwaarden
combined['Embarked'].fillna('C', inplace=True)

# Verwerk 'Cabin' kolom
combined['Cabin'].fillna('M', inplace=True)
combined['Cabin'] = combined['Cabin'].str[0]
combined.loc[combined['Cabin'] == 'T', 'Cabin'] = 'M'  # Aanpassen 'T' naar 'M'

# 2. Categoriseren van 'Title' en extractie uit 'Name'
st.subheader("Stap 2: Extractie en Categorisatie van Titels")

# Splits 'Name' in voor- en achternaam en titel
names = combined['Name']
titles = names.apply(lambda name: name.split(', ')[1].split('. ')[0])
combined['Title'] = titles

# Groepeer titels
combined['Title'].replace(
    {'Capt': 'Military', 'Col': 'Military', 'Major': 'Military',
     'Don': 'Nobility', 'Dona': 'Nobility', 'Jonkheer': 'Nobility', 'Lady': 'Nobility', 
     'Sir': 'Nobility', 'the Countess': 'Nobility', 'Miss': 'Ms', 'Mlle': 'Ms', 'Ms': 'Ms',
     'Mme': 'Mrs', 'Mrs': 'Mrs'}, inplace=True)

st.write("Na de extractie en hercategorisatie hebben we de volgende titels:")
st.write(combined['Title'].value_counts())

# 3. Age Binning
st.subheader("Stap 3: Leeftijd Categoriseren")

# Voeg Age_bins toe
bins = np.arange(0, 90, 10)
combined['Age_Bin'] = pd.cut(combined['Age'], bins)
st.write("Voor het model hebben we leeftijden gegroepeerd in leeftijdscategorieën (bijv., 0-10, 10-20, etc.) om patronen beter te herkennen.")
st.write(combined[['Age', 'Age_Bin']].head(10))

# 4. Berekening van Fare per ticket en fare bins
st.subheader("Stap 4: Fare-per-Ticket berekenen en categoriseren")

# Ticket-aantallen per ticketnummer
ticket_counts = combined['Ticket'].value_counts()
combined['Ticket_Count'] = combined['Ticket'].map(ticket_counts)

# Bereken fare per ticket
combined['Fare_per_Ticket'] = combined['Fare'] / combined['Ticket_Count']
combined['Fare_Bin'] = pd.cut(combined['Fare_per_Ticket'], [0, 20, 40, 60, 80, 150])

st.write("Na de berekening hebben we de vervoersprijzen in categorieën gegroepeerd om de impact van prijsverschillen beter te kunnen analyseren.")

# Toon voorbeeld van de gewijzigde kolommen
st.write("Voorbeeld van de gewijzigde dataset:")
st.write(combined[['Fare', 'Ticket', 'Ticket_Count', 'Fare_per_Ticket', 'Fare_Bin']].head(10))

# 5. Berekening familiegrootte
st.subheader("Stap 5: Berekenen van Familie Grootte")

# Voeg 'Num_Family' kolom toe
combined['Num_Family'] = combined['SibSp'] + combined['Parch'] + 1

st.write("De familieomvang is berekend door het aantal ouders en broers/zussen samen te voegen.")
st.write(combined[['SibSp', 'Parch', 'Num_Family']].head(10))

# 6. Onnodige kolommen verwijderen
st.subheader("Stap 6: Verwijderen van Onnodige Kolommen")

combined.drop(['Name', 'Age', 'Ticket', 'Fare', 'Ticket_Count', 'Fare_per_Ticket'], axis=1, inplace=True)
st.write("De volgende kolommen zijn verwijderd, omdat ze niet direct nodig zijn voor het model: `Name`, `Age`, `Ticket`, `Fare`, `Ticket_Count`, `Fare_per_Ticket`.")

# Nieuwe training- en testset maken
new_train = combined.iloc[:891]
new_test = combined.iloc[891:]
new_train['Survived'] = survived

# Eindige dataset
st.subheader("Gereed voor Modeltraining")
st.write("Hieronder ziet u de eerste paar rijen van de voorbereide dataset die gebruikt kan worden voor training.")
st.write(new_train.head())

st.write("""
**Samenvatting:**  
Elke stap in deze voorbereiding helpt ons om belangrijke kenmerken voor machine learning te verbeteren en irrelevante of 
verwarrende gegevens te verwijderen. Dit verbetert de nauwkeurigheid en prestaties van een Random Forest-model.
""")

