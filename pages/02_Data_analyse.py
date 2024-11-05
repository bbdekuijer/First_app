import streamlit as st
import pandas as pd
import plotly.express as px

# Laad de dataset
train = pd.read_csv('Data/Raw/train.csv')
test = pd.read_csv('Data/Raw/test.csv')

#training dataset has a 'survived' column. We will save this one as a variable. 
survived = train['Survived']

#we drop the 'survived' column from the train dataset. 
train = train.drop(['Survived'], axis=1)

# we extract the passenger IDs from both datasets. 
train_ID = train['PassengerId']
test_ID = test['PassengerId']

#here we combine the IDs from the two datasets and clean up the index. 
combined = pd.concat([train,test]).reset_index(drop=True)

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

# Count of NaN values in each column
nan_counts = combined.isnull().sum()
nan_data = pd.DataFrame({'Column': nan_counts.index, 'NaN Count': nan_counts.values})

# Display NaN count as a table
st.subheader("Aantal Missende Waarden per Kolom")
st.write(nan_data)

