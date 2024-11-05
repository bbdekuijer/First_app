import streamlit as st
import pandas as pd
import plotly.express as px

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Titel van de visualisatie sectie
st.title("Visualisatie van gegevens Titanic Dataset")

# Maak twee kolommen voor de data en de statistieken
col1, col2 = st.columns(2)

# Eerste kolom voor de eerste paar rijen van de dataset
with col1:
    st.subheader("Gegevens")
    st.dataframe(data.head(8))  # Laat de eerste 8 rijen van de dataset zien

# Tweede kolom voor de basisstatistieken
with col2:
    st.subheader("Basis Statistieken")
    st.write(data.describe())  # Basisstatistieken van de dataset

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

# Sectie voor NaN-verdeling met staafdiagram
st.subheader("Verdeling van Missende Waarden per Kolom")

# Maak een dataframe dat telt hoeveel NaN's er in elke kolom zitten
nan_data = pd.DataFrame(data.isna().sum(), columns=['NaN Count']).reset_index()
nan_data.columns = ['Column', 'NaN Count']

# Maak een staafdiagram voor de NaN-waarden
fig_nan_bar = px.bar(nan_data, x='Column', y='NaN Count', title="Aantal Missende Waarden per Kolom")
fig_nan_bar.update_layout(
    xaxis_title="Kolommen",
    yaxis_title="Aantal Missende Waarden",
    showlegend=False
)
st.plotly_chart(fig_nan_bar)

# Titel voor leeftijdsdistributie en passagiersklasse-selectiebox
st.subheader("Leeftijdsdistributie per Passagiersklasse")
pclass_options = sorted(data['Pclass'].unique())
pclass = st.selectbox("Selecteer een passagiersklasse:", pclass_options)

# Filter de data op basis van de geselecteerde klasse en verwijder NaN-waarden in de Age kolom
filtered_data = data[(data['Pclass'] == pclass) & (data['Age'].notna())]

# Checkboxen voor het weergeven van de histogram en boxplot
show_histogram = st.checkbox("Toon Histogram")
show_boxplot = st.checkbox("Toon Boxplot")

# Als histogram geselecteerd is, maak en toon de histogram
if show_histogram:
    fig_age_hist = px.histogram(
        filtered_data,
        x='Age',
        title=f"Leeftijdsdistributie voor Passagiers in Klasse {pclass}",
        labels={'Age': 'Leeftijd'},
        color='Survived',
        color_discrete_sequence=['#FFA07A', '#90EE90'],  # Kleuren: zacht oranje en lichtgroen
        category_orders={'Survived': [0, 1]}
    )
    # Forceer de bin-grootte op 5 (zodat 80/5 = 16 bins) en stel de x-as vast van 0 tot 80
    fig_age_hist.update_traces(xbins=dict(start=0, end=80, size=5))
    fig_age_hist.update_layout(
        legend_title_text='Overleving',
        xaxis_title='Leeftijd',
        yaxis_title='Aantal Passagiers',
        xaxis=dict(range=[0, 80])  # Stel de x-as limiet vast van 0 tot 80
    )
    st.plotly_chart(fig_age_hist)

# Als boxplot geselecteerd is, maak en toon de boxplot
if show_boxplot:
    fig_age_box = px.box(
        filtered_data,
        y='Age',
        title=f"Leeftijdsverdeling voor Passagiers in Klasse {pclass}",
        color_discrete_sequence=['#4682B4']  # Zachte blauwe kleur voor de boxplot
    )
    fig_age_box.update_layout(
        xaxis_title="",
        yaxis_title="Leeftijd"
    )
    st.plotly_chart(fig_age_box)

# Vervang de afkortingen in de 'Embarked' kolom met de volledige haven namen
data['Embarked_Full'] = data['Embarked'].map({'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'})

# Verwijder eventueel missende waarden in de 'Embarked' kolom om fouten te voorkomen
data = data.dropna(subset=['Embarked_Full'])

# Hoofdtitel
st.subheader("Titanic Data Analyse - Passagiers per Haven")

# Informatie sectie over de grafiek
st.write("Deze grafiek toont hoeveel passagiers uit elke haven aan boord van de Titanic gingen.")

# Barplot voor aantal passagiers per haven
fig_embarked = px.bar(
    data['Embarked_Full'].value_counts(),
    labels={'index': 'Haven', 'value': 'Aantal Passagiers'},
    title="Aantal Passagiers per Haven van Vertrek",
    color_discrete_sequence=['#4682B4']  # Zachte blauwe kleur
)

# Grafiek instellingen
fig_embarked.update_layout(
    xaxis_title="Haven van Vertrek",
    yaxis_title="Aantal Passagiers",
    showlegend=False
)

# Grafiek weergeven in Streamlit
st.plotly_chart(fig_embarked)
