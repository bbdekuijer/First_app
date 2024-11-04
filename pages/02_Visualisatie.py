import streamlit as st
import pandas as pd
import plotly.express as px

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Titel van de visualisatie sectie
st.title("Interactieve Visualisatie van Overlevingsstatistieken")

# Selectiebox voor grafiektype
chart_type = st.selectbox("Selecteer de grafiek die je wilt zien:", 
                           ["Overleving op basis van Geslacht", 
                            "Overleving op basis van Passagiersklasse", 
                            "Leeftijdsverdeling van Overlevenden en Niet-Overlevenden"])

# Grafiek weergeven op basis van de selectie
if chart_type == "Overleving op basis van Geslacht":
    fig_gender = px.histogram(data, x='Sex', color='Survived', 
                               title="Overleving op basis van Geslacht", 
                               labels={'Sex': 'Geslacht', 'Survived': 'Overleefd'},
                               color_discrete_map={0: 'orange', 1: 'blue'},  # Aangepaste kleuren
                               barmode='group')
    st.plotly_chart(fig_gender)

elif chart_type == "Overleving op basis van Passagiersklasse":
    fig_class = px.histogram(data, x='Pclass', color='Survived', 
                              title="Overleving op basis van Passagiersklasse",
                              labels={'Pclass': 'Klasse', 'Survived': 'Overleefd'},
                              color_discrete_map={0: 'orange', 1: 'blue'},  # Aangepaste kleuren
                              barmode='group')
    st.plotly_chart(fig_class)

elif chart_type == "Leeftijdsverdeling van Overlevenden en Niet-Overlevenden":
    fig_age = px.histogram(data, x='Age', color='Survived', 
                            title="Leeftijdsverdeling van Overlevenden",
                            labels={'Age': 'Leeftijd', 'Survived': 'Overleefd'},
                            color_discrete_map={0: 'orange', 1: 'blue'},  # Aangepaste kleuren
                            marginal='box')  # Voeg boxplot toe voor extra inzicht
    st.plotly_chart(fig_age)
