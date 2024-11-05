import streamlit as st

# Hoofdtitel
st.title("Titanic Data Analyse App")

# Introductie
st.write("Welkom bij de Titanic Data Analyse App! Deze app biedt een interactieve manier om de Titanic-dataset te verkennen, visualiseren en te analyseren.")
st.write("""
Met behulp van deze app kun je:
- Basisstatistieken van de dataset bekijken.
- Visualisaties genereren over leeftijdsverdeling, passagiersklassen en overlevingskansen.
- Diepgaand analyseren wie er aan boord waren en waar ze vandaan kwamen.

Duik erin en ontdek zelf de patronen en inzichten die de Titanic-data te bieden heeft!
""")

# Afbeelding onderaan de pagina
st.image("Afbeeldingen/Titanic.jpg", caption="Titanic", use_column_width=True)

