import streamlit as st
import pandas as pd
import plotly.express as px

# Titel en Introductie
st.title("Model Resultaten en Inzichten")
st.write("""
Op deze pagina presenteren we de uiteindelijke voorspellingen van ons getrainde model. De onderstaande tabel geeft de overlevingskansen weer op basis van de kenmerken van de passagiers.
""")

# Laad de voorspellingen vanuit het submission-bestand
file_path = "Data/Edit/submission_verbeterd.csv"
predictions_df = pd.read_csv(file_path)

# Tabelweergave van de volledige dataset
st.write("Hier zijn de voorspellingen van ons model:")
st.dataframe(predictions_df)  # Toon de volledige dataset

# Grafiek: Verdeling van overlevenden
st.write("Verdeling van de voorspelde overlevingskansen:")
survived_counts = predictions_df['Survived'].value_counts().sort_index()
fig_survived = px.bar(
    survived_counts,
    x=survived_counts.index,
    y=survived_counts.values,
    labels={'x': 'Survived (0 = Nee, 1 = Ja)', 'y': 'Aantal Passagiers'},
    title="Aantal Overlevenden vs. Niet-Overlevenden",
    orientation='h',
    color=survived_counts.index
)
fig_survived.update_layout(showlegend=False, xaxis_title="Overleving (0 = Nee, 1 = Ja)", yaxis_title="Aantal Passagiers")
st.plotly_chart(fig_survived)

# Extra analyses per kenmerk
st.subheader("Overleving op Basis van Verschillende Eigenschappen")
analysis_type = st.selectbox("Selecteer een kenmerk om te analyseren:", ["Geslacht", "Leeftijdsgroep", "Vertrekhaven (Embarked)"])

if analysis_type == "Geslacht":
    sex_counts = predictions_df.groupby(['Sex', 'Survived']).size().unstack()
    fig_sex = px.bar(
        sex_counts,
        barmode='group',
        title="Overleving per Geslacht",
        labels={'value': 'Aantal Passagiers', 'Sex': 'Geslacht', 'Survived': 'Overleefd'},
        color_discrete_sequence=px.colors.qualitative.Set1
    )
    st.plotly_chart(fig_sex)

elif analysis_type == "Leeftijdsgroep":
    # Maak leeftijdsgroepen aan
    bins = [0, 12, 18, 35, 50, 80]
    labels = ['Kind', 'Tiener', 'Volwassene', 'Middelbare Leeftijd', 'Senior']
    predictions_df['AgeGroup'] = pd.cut(predictions_df['Age'], bins=bins, labels=labels)
    
    age_counts = predictions_df.groupby(['AgeGroup', 'Survived']).size().unstack()
    fig_age = px.bar(
        age_counts,
        barmode='group',
        title="Overleving per Leeftijdsgroep",
        labels={'value': 'Aantal Passagiers', 'AgeGroup': 'Leeftijdsgroep', 'Survived': 'Overleefd'},
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    st.plotly_chart(fig_age)

elif analysis_type == "Vertrekhaven (Embarked)":
    predictions_df['Embarked'] = predictions_df['Embarked'].map({'S': 'Southampton', 'C': 'Cherbourg', 'Q': 'Queenstown'})
    
    embarked_counts = predictions_df.groupby(['Embarked', 'Survived']).size().unstack()
    fig_embarked = px.bar(
        embarked_counts,
        barmode='group',
        title="Overleving per Vertrekhaven",
        labels={'value': 'Aantal Passagiers', 'Embarked': 'Vertrekhaven', 'Survived': 'Overleefd'},
        color_discrete_sequence=px.colors.qualitative.Vivid
    )
    st.plotly_chart(fig_embarked)

# Samenvatting
st.subheader("Conclusie")
st.write("""
Deze resultaten zijn gebaseerd op het model en de voorafgaande datatransformatie. We hebben gezien dat passagiers in hogere klassen en jongere passagiers vaker overleefden. 
Deze voorspellingen bieden inzicht in hoe kenmerken de overlevingskans op de Titanic beïnvloeden.
""")

# Afbeelding onderaan de pagina
st.image("Afbeeldingen/Uitkomst.jpg", caption="Titanic", use_column_width=True)
