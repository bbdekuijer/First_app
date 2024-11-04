import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Titel van de Streamlit-app
st.title("Titanic Missing Values Visualizer")

# Laad de train en test datasets
train_data_path = "Data/Raw/train.csv"
test_data_path = "Data/Raw/test.csv"

# Laad de datasets
train_data = pd.read_csv(train_data_path)
test_data = pd.read_csv(test_data_path)

# Functie om ontbrekende waarden te berekenen
def get_missing_values(data):
    missing_values = data.isnull().sum()
    missing_df = pd.DataFrame({
        "Column": missing_values.index,
        "Missing Values": missing_values.values
    })
    return missing_df

# Ontbrekende waarden voor trainingsset
train_missing_df = get_missing_values(train_data)

# Ontbrekende waarden voor testset
test_missing_df = get_missing_values(test_data)

# Combineer de resultaten voor een betere visualisatie
combined_missing_df = pd.DataFrame({
    "Column": train_missing_df['Column'],
    "Train Missing Values": train_missing_df['Missing Values'],
    "Test Missing Values": test_missing_df['Missing Values'].reindex(train_missing_df['Column'])
})

# Plotly interactieve bar plot voor ontbrekende waarden in de trainset
fig_train = px.bar(
    train_missing_df, 
    x="Column", 
    y="Missing Values",
    title="Aantal Ontbrekende Waarden in de Trainingsset",
    labels={"Column": "Kolomnaam", "Missing Values": "Aantal Ontbrekende Waarden"},
    template="plotly_white"
)

# Plotly interactieve bar plot voor ontbrekende waarden in de testset
fig_test = px.bar(
    test_missing_df, 
    x="Column", 
    y="Missing Values",
    title="Aantal Ontbrekende Waarden in de Testset",
    labels={"Column": "Kolomnaam", "Missing Values": "Aantal Ontbrekende Waarden"},
    template="plotly_white"
)

# Toon de plots in Streamlit
st.plotly_chart(fig_train)
st.plotly_chart(fig_test)

# Optioneel: Toon de eerste paar rijen van de datasets
st.write("Voorbeeld Trainingsset:")
st.dataframe(train_data.head())
st.write("Voorbeeld Testset:")
st.dataframe(test_data.head())
