import streamlit as st
import pandas as pd

# Titel en Introductie
st.title("Model Resultaten en Inzichten")
st.write("""
Op deze pagina presenteren we de uiteindelijke voorspellingen van ons getrainde model. De onderstaande tabel geeft de overlevingskansen weer op basis van de kenmerken van de passagiers.
""")

# Laad de voorspellingen vanuit het submission-bestand
file_path = "Data/Edit/submission_verbeterd.csv"
try:
    predictions_df = pd.read_csv(file_path)
    st.write("Hier zijn de voorspellingen van ons model:")
    st.write(predictions_df.head(10))  # Toon de eerste 10 rijen als voorbeeld

    # Voeg eventueel statistieken toe over de voorspellingen
    survived_counts = predictions_df['Survived'].value_counts()
    st.write("Verdeling van de voorspelde overlevingskansen:")
    st.bar_chart(survived_counts)

    # Samenvatting
    st.subheader("Conclusie")
    st.write("""
    Deze resultaten zijn gebaseerd op het model en de voorafgaande datatransformatie. We hebben gezien dat passagiers in hogere klassen en jongere passagiers vaker overleefden. 
    Deze voorspellingen bieden inzicht in hoe kenmerken de overlevingskans op de Titanic beïnvloeden.
    """)
except FileNotFoundError:
    st.error(f"Het bestand `{file_path}` kon niet worden gevonden. Zorg ervoor dat het bestand op de juiste locatie staat.")
