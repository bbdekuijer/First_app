import streamlit as st

# Titel van de hoofdpagina
st.title("Amsterdam Stemmen")

# Sidebar voor het navigeren naar verschillende stadsdelen
st.sidebar.title("Kies een regio")
region_page = st.sidebar.selectbox("Selecteer een stadsdeel", [
    "Centrum",
    "West",
    "Zuid",
    "Zuidoost",
    "Oost",
    "Noord",
    "Nieuw-West"
])

# Afhankelijk van de keuze, importeer je de juiste module voor het stadsdeel
if region_page == "Centrum":
    # Voeg hier de code of functie voor Centrum in
    import 01_Centrum  # Zorg ervoor dat de naam van de file klopt
elif region_page == "West":
    import 02_West
elif region_page == "Zuid":
    import 03_Zuid
elif region_page == "Zuidoost":
    import 04_Zuidoost
elif region_page == "Oost":
    import 05_Oost
elif region_page == "Noord":
    import 06_Noord
elif region_page == "Nieuw-West":
    import 07_Nieuw_West
