import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your metro datasets for different years
@st.cache
def load_data():
    data = {}
    data['2017'] = pd.read_csv('.devcontainer/2017_Entry_Exit.csv')
    data['2016'] = pd.read_csv('.devcontainer/2016_Entry_Exit.csv')
    data['2015'] = pd.read_csv('.devcontainer/2015_Entry_Exit.csv')
    data['2014'] = pd.read_csv('.devcontainer/2014_Entry_Exit.csv')
    data['2013'] = pd.read_csv('.devcontainer/2013_Entry_Exit.csv')
    data['2012'] = pd.read_csv('.devcontainer/2012_Entry_Exit.csv')
    data['2011'] = pd.read_csv('.devcontainer/2011_Entry_Exit.csv')
    data['2010'] = pd.read_csv('.devcontainer/2010_Entry_Exit.csv')
    data['2009'] = pd.read_csv('.devcontainer/2009_Entry_Exit.csv')
    data['2008'] = pd.read_csv('.devcontainer/2008_Entry_Exit.csv')
    data['2007'] = pd.read_csv('.devcontainer/2007_Entry_Exit.csv')
    return data

metro_data_dict = load_data()

# Create a slider in the sidebar for year selection
st.sidebar.title("Select Year")
selected_year = st.sidebar.slider('Year', min_value=2007, max_value=2017, step=1, value=2017)

# Load the data for the selected year
metro_data = metro_data_dict[str(selected_year)]

# Summarize total usage for each station
metro_data['total_usage'] = metro_data['Entry_Week'] + metro_data['Entry_Saturday'] + metro_data['Entry_Sunday']

# Sort by total usage and select the top 25 busiest stations
top_25_stations = metro_data[['Station', 'total_usage']].sort_values(by='total_usage', ascending=False).head(25)

# Plot the top 25 busiest stations
st.title(f'Top 25 Busiest Stations in London - {selected_year}')
fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(top_25_stations['Station'], top_25_stations['total_usage'], color='steelblue')
ax.set_xlabel('Total Metro Usage')
ax.set_ylabel('Stations')
ax.set_title(f'Top 25 Busiest Stations in London - {selected_year}')
ax.invert_yaxis()  # Invert the y-axis to display the busiest station on top
st.pyplot(fig)

# Find peak times for each station by comparing weekday vs. weekend
metro_data['peak_time'] = metro_data[['Entry_Week', 'Entry_Saturday', 'Entry_Sunday']].idxmax(axis=1)

# Get peak times for the top 25 stations
top_25_stations_with_peak = metro_data[metro_data['Station'].isin(top_25_stations['Station'])][['Station', 'peak_time']]

# Display the top 25 stations with peak times
st.subheader(f'Top 25 Stations with Peak Times - {selected_year}')
st.write(top_25_stations_with_peak)
