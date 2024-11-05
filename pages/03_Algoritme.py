import streamlit as st
import pandas as pd
import plotly.express as px

# Titel en Introductie
st.title("Model Resultaten en Inzichten")
st.write("""
Op deze pagina presenteren we de uiteindelijke voorspellingen van ons getrainde model. De onderstaande tabel toont de overlevingskansen per passagier, samen met hun kenmerken.
""")

# Laad de voorspellingen vanuit het submission-bestand
file_path = "Data/Edit/submission_verbeterd.csv"
predictions_df = pd.read_csv(file_path)

# Toon de volledige dataset van de voorspellingen
st.write("Hier zijn alle voorspellingen van ons model:")
st.dataframe(predictions_df)  # Toon de volledige dataset als scrollbare tabel

# Verdeling van voorspelde overlevingskansen
st.subheader("Verdeling van de voorspelde overlevingskansen")
survived_counts = predictions_df['Survived'].value_counts()
fig = px.bar(survived_counts, orientation='h', labels={'index': 'Survival Status', 'value': 'Aantal Passagiers'},
             title="Aantal Overlevenden vs Niet-overlevenden")
fig.update_layout(yaxis=dict(tickvals=[0, 1], ticktext=['Niet Overleefd', 'Overleefd']))
st.plotly_chart(fig)

# Visualisatie: Verdeling naar geslacht en overleving
st.subheader("Overleving op basis van Geslacht")
gender_survival = predictions_df.groupby(['Sex', 'Survived']).size().reset_index(name='Aantal')
fig_gender = px.bar(gender_survival, x='Sex', y='Aantal', color='Survived', barmode='group',
                    labels={'Survived': 'Overleefd', 'Aantal': 'Aantal Passagiers'},
                    title="Overleving op basis van Geslacht")
fig_gender.update_layout(xaxis_title="Geslacht", yaxis_title="Aantal Passagiers",
                         legend=dict(title="Overleving Status", tickvals=[0, 1], ticktext=['Niet Overleefd', 'Overleefd']))
st.plotly_chart(fig_gender)

# Visualisatie: Verdeling naar leeftijdsgroep en overleving
st.subheader("Overleving op basis van Leeftijdsgroepen")
# Voeg een leeftijdsgroep-kolom toe voor eenvoudiger visualiseren
age_bins = [0, 12, 18, 30, 40, 60, 80]
age_labels = ['0-12', '13-18', '19-30', '31-40', '41-60', '60+']
predictions_df['Leeftijdsgroep'] = pd.cut(predictions_df['Age'], bins=age_bins, labels=age_labels)

age_survival = predictions_df.groupby(['Leeftijdsgroep', 'Survived']).size().reset_index(name='Aantal')
fig_age = px.bar(age_survival, x='Leeftijdsgroep', y='Aantal', color='Survived', barmode='group',
                 labels={'Leeftijdsgroep': 'Leeftijdsgroep', 'Aantal': 'Aantal Passagiers'},
                 title="Overleving op basis van Leeftijdsgroepen")
fig_age.update_layout(xaxis_title="Leeftijdsgroep", yaxis_title="Aantal Passagiers",
                      legend=dict(title="Overleving Status", tickvals=[0, 1], ticktext=['Niet Overleefd', 'Overleefd']))
st.plotly_chart(fig_age)

# Visualisatie: Verdeling naar inschepingslocatie (Embarked) en overleving
st.subheader("Overleving op basis van Inschepingslocatie (Embarked)")
embarked_survival = predictions_df.groupby(['Embarked', 'Survived']).size().reset_index(name='Aantal')
fig_embarked = px.bar(embarked_survival, x='Embarked', y='Aantal', color='Survived', barmode='group',
                      labels={'Embarked': 'Inschepingslocatie', 'Aantal': 'Aantal Passagiers'},
                      title="Overleving op basis van Inschepingslocatie (Embarked)")
fig_embarked.update_layout(xaxis_title="Inschepingslocatie", yaxis_title="Aantal Passagiers",
                           legend=dict(title="Overleving Status", tickvals=[0, 1], ticktext=['Niet Overleefd', 'Overleefd']))
st.plotly_chart(fig_embarked)

# Samenvatting
st.subheader("Conclusie")
st.write("""
Deze resultaten laten zien hoe verschillende kenmerken de overlevingskans op de Titanic beïnvloeden.  
We zien dat bijvoorbeeld geslacht, leeftijdsgroep, en inschepingslocatie een rol spelen in de overlevingskans.  
Deze inzichten kunnen ons helpen bij het begrijpen van de factoren die bijdroegen aan de overleving tijdens de ramp.
""")

# Afbeelding onderaan de pagina
st.image("Afbeeldingen/Uitkomst.jpg", caption="Titanic", use_column_width=True)

