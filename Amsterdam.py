# Check je huidige working directory
import os
print(os.getcwd())

# Pas je working directory aan indien gewenst
path = 'C:\\Users\\bbdek\\Downloads' # zet hier wat voor jou goed is
os.chdir(path)

stemmen_ams= pd.read_csv('2021 stemmen Amsterdam.csv')

import streamlit as st

# Maak kolommen aan
col1, col2 = st.columns([3, 1])  # col1 is breder, col2 is smaller (voor legenda)

# In col2 (rechter kolom) plaatsen we de legenda
with col2:
    st.subheader('Legenda')
    st.write("""
    - **Dropdown Menu:** kies een regio uit de lijst.
    - **Slider:** Verschuif de slider om het aantal partijen te kiezen tussen 0 en 33.
    - **Checkbox:** Vink deze aan om extra informatie te tonen.
    """)

# In col1 (linker kolom) plaatsen we de interactieve widgets
with col1:
    # Dropdown menu
    opties = ["amsterdam", "centrum", "oost", "zuid", "west", "noord",  "nieuw_west", "zuidoost" ]
    geselecteerde_optie = st.selectbox('Kies een regio:', opties)
    st.write(f"Geselecteerde regio: {geselecteerde_optie}")
  # Navigatie logica gebaseerd op de geselecteerde regio
    if geselecteerde_optie == "amsterdam":
        st.subheader("Welkom in Amsterdam!")
        st.write("""
        Amsterdam is de hoofdstad van Nederland en bekend om zijn grachten, musea, 
        en rijke geschiedenis. Het is een diverse stad met verschillende wijken die
        elk hun eigen karakter hebben.
        """)

    elif geselecteerde_optie == "centrum":
        st.subheader("Welkom in het Centrum van Amsterdam!")
        st.write("""
        Het centrum van Amsterdam is het oudste en meest toeristische deel van de stad. 
        Het is bekend om de prachtige grachten, historische gebouwen, het Koninklijk Paleis,
        de Dam en het Anne Frank Huis.
        """)

    elif geselecteerde_optie == "oost":
        st.subheader("Welkom in Amsterdam Oost!")
        st.write("""
        Amsterdam Oost is een diverse wijk met zowel traditionele als moderne architectuur. 
        Het Oosterpark en Artis zijn bekende trekpleisters, evenals de culturele smeltkroes 
        van de Dappermarkt.
        """)

    elif geselecteerde_optie == "zuid":
        st.subheader("Welkom in Amsterdam Zuid!")
        st.write("""
        Amsterdam Zuid staat bekend om het Museumplein, waar je het Rijksmuseum, 
        Van Gogh Museum en het Stedelijk Museum kunt vinden. Het is een van de luxere wijken 
        van de stad, met veel winkels en restaurants.
        """)

    elif geselecteerde_optie == "west":
        st.subheader("Welkom in Amsterdam West!")
        st.write("""
        Amsterdam West is een diverse buurt met een mix van culturen. Het Westerpark 
        is een populaire ontmoetingsplek, en de wijk staat bekend om zijn gezellige markten 
        en restaurants.
        """)

    elif geselecteerde_optie == "noord":
        st.subheader("Welkom in Amsterdam Noord!")
        st.write("""
        Amsterdam Noord is een snelgroeiend deel van de stad. Vroeger een industriële zone, 
        maar tegenwoordig bekend om moderne wijken en culturele hotspots zoals de NDSM-werf.
        """)

    elif geselecteerde_optie == "nieuw_west":
        st.subheader("Welkom in Amsterdam Nieuw-West!")
        st.write("""
        Amsterdam Nieuw-West is een van de grootste stadsdelen van de stad. Het biedt veel 
        ruimte en groen, en er zijn veel nieuwbouwwoningen. Het Sloterpark en Sloterplas zijn 
        favoriete recreatiegebieden.
        """)

    elif geselecteerde_optie == "zuidoost":
        st.subheader("Welkom in Amsterdam Zuidoost!")
        st.write("""
        Amsterdam Zuidoost is een multiculturele wijk en bekend vanwege de Johan Cruijff Arena, 
        het winkelcentrum de Amsterdamse Poort, en diverse concertzalen zoals de Ziggo Dome en AFAS Live.
        """)



# Vooraf voorbereide lijst met partijen en stemmen
parties = [
    'D66',  # 99649
    'VVD',  # 55445
    'GROENLINKS',  # 44907
    'Partij van de Arbeid (P.v.d.A.)',  # 32783
    'Partij voor de Dieren',  # 30880
    'DENK',  # 29384
    'Volt',  # 25988
    'BIJ1',  # 25563
    'PVV (Partij voor de Vrijheid)',  # 22180
    'SP (Socialistische Partij)',  # 21478
    'Forum voor Democratie',  # 11971
    'CDA',  # 10815
    'ChristenUnie',  # 6214
    'JA21',  # 5282
    'NIDA',  # 5053
    '50PLUS',  # 2355
    'JONG',  # 1278
    'CODE ORANJE',  # 864
    'Staatkundig Gereformeerde Partij (SGP)',  # 586
    'Piratenpartij',  # 391
    'Trots op Nederland (TROTS)',  # 384
    'LP (Libertaire Partij)',  # 383
    'Splinter',  # 343
    'JEZUS LEEFT',  # 301
    'NLBeter',  # 297
    'BBB',  # 276
    'OPRECHT',  # 247
    'U-Buntu Connected Front',  # 221
    'Partij voor de Republiek',  # 151
    'De Groenen',  # 151
    'Partij van de Eenheid',  # 144
    'Lijst Henk Krol',  # 106
    'Vrij en Sociaal Nederland'  # 89
]

votes = [
    99649,  # D66
    55445,  # VVD
    44907,  # GROENLINKS
    32783,  # Partij van de Arbeid (P.v.d.A.)
    30880,  # Partij voor de Dieren
    29384,  # DENK
    25988,  # Volt
    25563,  # BIJ1
    22180,  # PVV (Partij voor de Vrijheid)
    21478,  # SP (Socialistische Partij)
    11971,  # Forum voor Democratie
    10815,  # CDA
    6214,   # ChristenUnie
    5282,   # JA21
    5053,   # NIDA
    2355,   # 50PLUS
    1278,   # JONG
    864,    # CODE ORANJE
    586,    # Staatkundig Gereformeerde Partij (SGP)
    391,    # Piratenpartij
    384,    # Trots op Nederland (TROTS)
    383,    # LP (Libertaire Partij)
    343,    # Splinter
    301,    # JEZUS LEEFT
    297,    # NLBeter
    276,    # BBB
    247,    # OPRECHT
    221,    # U-Buntu Connected Front
    151,    # Partij voor de Republiek
    151,    # De Groenen
    144,    # Partij van de Eenheid
    106,    # Lijst Henk Krol
    89      # Vrij en Sociaal Nederland
]

# DataFrame maken
parties_df = pd.DataFrame({'Party': parties, 'Votes': votes})

# Slider om het aantal partijen te selecteren
num_parties = st.slider('Selecteer het aantal partijen om mee te rekenen:', min_value=1, max_value=len(parties), value=10)

# Sorteren op stemmen en top partijen tonen op basis van de selectie
top_parties = parties_df.sort_values(by='Votes', ascending=False).head(num_parties)

# Resultaten tonen
st.write(f"De top {num_parties} partijen op basis van stemmen zijn:")
st.write(top_parties)

