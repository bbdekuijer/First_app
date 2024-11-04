import streamlit as st
import pandas as pd
import plotly.express as px

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Titel van de visualisatie sectie
st.title("Interactieve Visualisatie van Overlevingsstatistieken")

# Histogram van overleving op basis van geslacht
st.subheader("Overleving op basis van Geslacht")
fig_gender = px.histogram(data, x='Sex', color='Survived', 
                           title="Overleving op basis van Geslacht", 
                           labels={'Sex': 'Geslacht', 'Survived': 'Overleefd'},
                           color_discrete_map={0: 'red', 1: 'green'},
                           barmode='group')
st.plotly_chart(fig_gender)

# Histogram van overleving op basis van Passagiersklasse
st.subheader("Overleving op basis van Passagiersklasse")
fig_class = px.histogram(data, x='Pclass', color='Survived', 
                          title="Overleving op basis van Passagiersklasse",
                          labels={'Pclass': 'Klasse', 'Survived': 'Overleefd'},
                          color_discrete_map={0: 'red', 1: 'green'},
                          barmode='group')
st.plotly_chart(fig_class)

# Histogram van overleving op basis van Leeftijd
st.subheader("Leeftijdsverdeling van Overlevenden en Niet-Overlevenden")
fig_age = px.histogram(data, x='Age', color='Survived', 
                        title="Leeftijdsverdeling van Overlevenden",
                        labels={'Age': 'Leeftijd', 'Survived': 'Overleefd'},
                        color_discrete_map={0: 'red', 1: 'green'},
                        marginal='box')  # Voeg boxplot toe voor extra inzicht
st.plotly_chart(fig_age)

