import streamlit as st
import pandas as pd

# Titel en Introductie
st.title("Model Resultaten en Inzichten")
st.write("""
Op deze pagina presenteren we de uiteindelijke voorspellingen van ons getrainde model. 
De onderstaande tabel geeft de overlevingskansen weer op basis van de kenmerken van de passagiers.
""")

# Laad de voorspellingen vanuit het submission-bestand
file_path = "Data/Edit/submission_verbeterd.csv"
predictions_df = pd.read_csv(file_path)

# Toon de gehele dataframe
st.write("Hier zijn de voorspellingen van ons model:")
st.write(predictions_df)  # Toon het volledige dataframe

# Visualiseer de verdeling van de overlevenden
survived_counts = predictions_df['Survived'].value_counts().sort_index()

# Vervang 0 en 1 door de labels "Niet Overleefd" en "Overleefd"
survived_labels = {0: "Niet Overleefd", 1: "Overleefd"}
survived_counts.index = survived_counts.index.map(survived_labels)

# Maak een horizontale bar chart zodat de labels goed leesbaar zijn
st.write("Verdeling van de voorspelde overlevingskansen:")
st.bar_chart(survived_counts, use_container_width=True)

# Samenvatting
st.subheader("Conclusie")
st.write("""
Deze resultaten zijn gebaseerd op het model en de voorafgaande datatransformatie. 
De voorspellingen geven inzicht in hoe de overleving van passagiers werd beïnvloed door de kenmerken van het schip.
""")

# Afbeelding onderaan de pagina
st.image("Afbeeldingen/Uitkomst.jpg", caption="Titanic", use_column_width=True)

