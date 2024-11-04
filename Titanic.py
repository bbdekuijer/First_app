import streamlit as st
import pandas as pd
import plotly.express as px

# Titel van de Streamlit-app
st.title("Titanic Missing Values Visualizer")

# Specificeer het pad naar de train.csv dataset
data_path = "Data/Raw/train.csv"

# Laad de dataset
data = pd.read_csv(data_path)

# Bereken het aantal ontbrekende waarden per kolom
missing_values = data.isnull().sum()
missing_df = pd.DataFrame({
    "Column": missing_values.index,
    "Missing Values": missing_values.values
})

# Plotly interactieve bar plot voor ontbrekende waarden (inclusief kolommen zonder NaN's)
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

