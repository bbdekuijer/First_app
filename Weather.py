import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load your metro dataset
metro_data = pd.read_csv('/Users/casijnvantill/Desktop/Data Science/Cases/Week 6/2017_Entry_Exit.csv')

# Summarize total usage for each station
metro_data['total_usage'] = metro_data['Entry_Week'] + metro_data['Entry_Saturday'] + metro_data['Entry_Sunday']

# Sort by total usage and select the top 25 busiest stations
top_25_stations = metro_data[['Station', 'total_usage']].sort_values(by='total_usage', ascending=False).head(25)

# Plot the top 25 busiest stations
st.title('Top 25 Busiest Stations in London')
fig, ax = plt.subplots(figsize=(12, 8))
ax.barh(top_25_stations['Station'], top_25_stations['total_usage'], color='steelblue')
ax.set_xlabel('Total Metro Usage')
ax.set_ylabel('Stations')
ax.set_title('Top 25 Busiest Stations in London')
ax.invert_yaxis()  # Invert the y-axis to display the busiest station on top
st.pyplot(fig)

# Find peak times for each station by comparing weekday vs. weekend
metro_data['peak_time'] = metro_data[['Entry_Week', 'Entry_Saturday', 'Entry_Sunday']].idxmax(axis=1)

# Get peak times for the top 25 stations
top_25_stations_with_peak = metro_data[metro_data['Station'].isin(top_25_stations['Station'])][['Station', 'peak_time']]

# Display the top 25 stations with peak times
st.subheader('Top 25 Stations with Peak Times')
st.write(top_25_stations_with_peak)


# Load the weather dataset
weather_data= pd.read_csv('/Users/casijnvantill/Downloads/weather_london.csv')

# Rename the date column
weather_data.rename(columns={'Unnamed: 0': 'date'}, inplace=True)

# Convert the date column to datetime format
weather_data['date'] = pd.to_datetime(weather_data['date'])

# Extract the month and year from the date
weather_data['month'] = weather_data['date'].dt.month
weather_data['year'] = weather_data['date'].dt.year

# Group by month to get the total precipitation per month
monthly_precipitation = weather_data.groupby('month')['prcp'].sum()

# Plot the histogram of monthly precipitation
st.title('Monthly Precipitation in London')
fig2, ax2 = plt.subplots(figsize=(10, 6))
ax2.bar(monthly_precipitation.index, monthly_precipitation.values)
ax2.set_title('Monthly Precipitation in London')
ax2.set_xlabel('Month')
ax2.set_ylabel('Total Precipitation (mm)')
ax2.set_xticks(range(1, 13))
ax2.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
st.pyplot(fig2)

# Grouping the data by month to get average temperatures (tavg, tmin, tmax) per month
monthly_temperatures = weather_data.groupby('month')[['tavg', 'tmin', 'tmax']].mean()

# Plotting the monthly average, minimum, and maximum temperatures
st.title('Monthly Temperatures in London')
fig3, ax3 = plt.subplots(figsize=(10, 6))
ax3.plot(monthly_temperatures.index, monthly_temperatures['tavg'], label='Avg Temp', marker='o')
ax3.plot(monthly_temperatures.index, monthly_temperatures['tmin'], label='Min Temp', marker='o')
ax3.plot(monthly_temperatures.index, monthly_temperatures['tmax'], label='Max Temp', marker='o')
ax3.set_title('Monthly Temperatures in London')
ax3.set_xlabel('Month')
ax3.set_ylabel('Temperature (°C)')
ax3.set_xticks(range(1, 13))
ax3.set_xticklabels(['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'])
ax3.legend()
st.pyplot(fig3)




