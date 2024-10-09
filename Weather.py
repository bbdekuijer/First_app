import pandas as pd
import matplotlib.pyplot as plt

# Load your metro dataset
metro_data = pd.read_csv('/Users/casijnvantill/Desktop/Data Science/Cases/Week 6/2017_Entry_Exit.csv')

# Summarize total usage for each station
metro_data['total_usage'] = metro_data['Entry_Week'] + metro_data['Entry_Saturday'] + metro_data['Entry_Sunday']

# Sort by total usage and select the top 25 busiest stations
top_25_stations = metro_data[['Station', 'total_usage']].sort_values(by='total_usage', ascending=False).head(25)

# Plot the top 25 busiest stations
plt.figure(figsize=(12, 8))
plt.barh(top_25_stations['Station'], top_25_stations['total_usage'], color='steelblue')
plt.xlabel('Total Metro Usage')
plt.ylabel('Stations')
plt.title('Top 25 Busiest Stations in London')
plt.gca().invert_yaxis()  # Invert the y-axis to display the busiest station on top
plt.tight_layout()
plt.show()

# Find peak times for each station by comparing weekday vs. weekend
metro_data['peak_time'] = metro_data[['Entry_Week', 'Entry_Saturday', 'Entry_Sunday']].idxmax(axis=1)

# Get peak times for the top 25 stations
top_25_stations_with_peak = metro_data[metro_data['Station'].isin(top_25_stations['Station'])][['Station', 'peak_time']]

# Display the top 25 stations with peak times
print(top_25_stations_with_peak)



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
import matplotlib.pyplot as plt

plt.figure(figsize=(10, 6))
plt.bar(monthly_precipitation.index, monthly_precipitation.values)
plt.title('Monthly Precipitation in London')
plt.xlabel('Month')
plt.ylabel('Total Precipitation (mm)')
plt.xticks(ticks=range(1, 13), labels=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
])

# Display the plot
plt.show()


# Grouping the data by month to get average temperatures (tavg, tmin, tmax) per month
monthly_temperatures = weather_data.groupby('month')[['tavg', 'tmin', 'tmax']].mean()

# Plotting the monthly average, minimum, and maximum temperatures
plt.figure(figsize=(10, 6))
plt.plot(monthly_temperatures.index, monthly_temperatures['tavg'], label='Avg Temp', marker='o')
plt.plot(monthly_temperatures.index, monthly_temperatures['tmin'], label='Min Temp', marker='o')
plt.plot(monthly_temperatures.index, monthly_temperatures['tmax'], label='Max Temp', marker='o')

plt.title('Monthly Temperatures in London')
plt.xlabel('Month')
plt.ylabel('Temperature (°C)')
plt.xticks(ticks=range(1, 13), labels=[
    'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'
])
plt.legend()

# Display the plot
plt.show()



