import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Laad de dataset
data_path = "Data/Raw/train.csv"
data = pd.read_csv(data_path)

# Hoofdtitel
st.title("Visualisatie")

# Introductie
st.write("In deze sectie kun je grafieken en visualisaties bekijken.")

# Eenvoudig staafdiagram voor overleving
st.subheader("Aantal Overlevenden")
survived_counts = data['Survived'].value_counts()
fig, ax = plt.subplots()
ax.bar(['Niet Overleefd', 'Overleefd'], survived_counts, color=['red', 'green'])
ax.set_ylabel('Aantal Passagiers')
st.pyplot(fig)  # Toon de grafiek in de app

# Histogram van leeftijden
st.subheader("Leeftijdshistogram")
fig2, ax2 = plt.subplots()
ax2.hist(data['Age'].dropna(), bins=30, color='blue', alpha=0.7)
ax2.set_xlabel('Leeftijd')
ax2.set_ylabel('Aantal Passagiers')
st.pyplot(fig2)  # Toon de histogram in de app
