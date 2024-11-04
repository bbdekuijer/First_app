import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Titel van de Streamlit-app
st.title("Titanic Missing Values Visualizer")

# Specificeer het pad naar de train.csv dataset
data_path = os.path.join("Data", "Raw", "train.csv")

# Controleer of het bestand bestaat
if os.path.exists(data_path):
    # Laad de dataset
    data = pd.read_csv(data_path)
    
    # Bereken het aantal ontbrekende waarden per kolom
    missing_values = data.isnull().sum()
    missing_values = missing_values[missing_values > 0]  # Alleen kolommen met NaN's
    missing_df = pd.DataFrame({
        "Column": missing_values.index,
        "Missing Values": missing_values.values
    })
    
    # Plotly interactieve bar plot voor ontbrekende waarden
    fig = px.bar(
        missing_df, 
        x="Column", 
        y="Missing Values",
        title="Number of Missing Values per Column",
        labels={"Column": "Column Name", "Missing Values": "Count of Missing Values"},
        template="plotly_white"
    )

    # Toon de plot in Streamlit
    st.plotly_chart(fig)

    # Toon optioneel de eerste paar rijen van de dataset
    st.write("Sample Data:")
    st.dataframe(data.head())
else:
    st.error("train.csv file not found in Data/Raw directory. Please make sure the file is located at Data/Raw/train.csv.")
