import plotly.express as px

st.title("Visualisaties")

# Histogram van de leeftijd
fig_age = px.histogram(data, x='Age', nbins=30, title='Distributie van Leeftijd')
st.plotly_chart(fig_age)

# Boxplot van de leeftijd per overleving
fig_box = px.box(data, x='Survived', y='Age', title='Leeftijd per Overleving')
st.plotly_chart(fig_box)
