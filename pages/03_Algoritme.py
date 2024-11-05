import streamlit as st
import pandas as pd
import plotly.express as px

# Titel en Introductie
st.title("Model Resultaten en Inzichten")
st.write("""
Op deze pagina presenteren we de uiteindelijke voorspellingen van ons getrainde model. De onderstaande tabel toont de passagiersgegevens samen met hun kenmerken.
""")

# Laad de voorspellingen vanuit het submission-bestand
file_path = "Data/Edit/submission_verbeterd.csv"
predictions_df = pd.read_csv(file_path)

# Toon de volledige dataset van de voorspellingen
st.write("Hier zijn alle voorspellingen van ons model:")
st.dataframe(predictions_df)  # Toon de volledige dataset als scrollbare tabel

# Verdeling van passagiers per klasse (Pclass)
st.subheader("Verdeling van Passagiers per Klasse (Pclass)")
class_counts = predictions_df['Pclass'].value_counts().sort_index()
fig_class = px.bar(class_counts, x=class_counts.index, y=class_counts.values, labels={'x': 'Klasse', 'y': 'Aantal Passagiers'},
                   title="Aantal Passagiers per Klasse")
st.plotly_chart(fig_class)

# Verdeling van passagiers op basis van geslacht (Sex)
st.subheader("Verdeling van Passagiers per Geslacht")
gender_counts = predictions_df['Sex'].value_counts()
fig_gender = px.bar(gender_counts, x=gender_counts.index, y=gender_counts.values, labels={'x': 'Geslacht', 'y': 'Aantal Passagiers'},
                    title="Aantal Passagiers per Geslacht")
st.plotly_chart(fig_gender)

# Verdeling van passagiers per leeftijdsgroep (Age_Bin)
st.subheader("Verdeling van Passagiers per Leeftijdsgroep")
age_group_counts = predictions_df['Age_Bin'].value_counts().sort_index()
fig_age = px.bar(age_group_counts, x=age_group_counts.index, y=age_group_counts.values, labels={'x': 'Leeftijdsgroep', 'y': 'Aantal Passagiers'},
                 title="Aantal Passagiers per Leeftijdsgroep")
st.plotly_chart(fig_age)

# Verdeling van passagiers per inschepingslocatie (Embarked)
st.subheader("Verdeling van Passagiers per Inschepingslocatie (Embarked)")
embarked_counts = predictions_df['Embarked'].value_counts()
fig_embarked = px.bar(embarked_counts, x=embarked_counts.index, y=embarked_counts.values, labels={'x': 'Inschepingslocatie', 'y': 'Aantal Passagiers'},
                      title="Aantal Passagiers per Inschepingslocatie (Embarked)")
st.plotly_chart(fig_embarked)

# Samenvatting
st.subheader("Conclusie")
st.write("""
Deze resultaten bieden een overzicht van de passagierskenmerken zoals klasse, geslacht, leeftijdsgroep en inschepingslocatie.  
Deze inzichten kunnen ons helpen om patronen en verschillen in de dataset te herkennen.
""")

# Afbeelding onderaan de pagina
st.image("Afbeeldingen/Uitkomst.jpg", caption="Titanic", use_column_width=True)
