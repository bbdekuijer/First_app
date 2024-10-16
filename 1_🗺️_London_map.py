import streamlit as st
import plotly.graph_objects as go
import pandas as pd

# Load the data
sb = pd.read_csv('A5SBIntensiteit.csv')
nb = pd.read_csv('A5NBIntensiteit.csv')

# Filter for 'greaterThan 12.20' category
sb = sb[sb['voertuigcategorie'] == 'greaterThan 12.20']
nb = nb[nb['voertuigcategorie'] == 'greaterThan 12.20']

# Group and pivot the data
sb = sb.groupby(['start_meetperiode', 'id_meetlocatie']).agg('sum')['gem_intensiteit'].unstack(level='id_meetlocatie')
nb = nb.groupby(['start_meetperiode', 'id_meetlocatie']).agg('sum')['gem_intensiteit'].unstack(level='id_meetlocatie')

# Merge the dataframes
df = sb.merge(nb, on='start_meetperiode', how='inner')

# Rename columns
rename = {
    'RWS01_MONICA_00D005026028D0050005': 'SB voor afr 3',
    'RWS01_MONICA_00D005026028D0050009': 'SB voor afr 3_2',
    'RWS01_MONICA_00D005024C2FD0050005': 'SB tussen afop 3',
    'RWS01_MONICA_00D005024C2FD0050009': 'SB tussen afop 3_2',
    'RWS01_MONICA_00D005023C4AD0050005': 'SB na opr 3',
    'RWS01_MONICA_00D005023C4AD0050009': 'SB na opr 3_2',
    'RWS01_MONICA_00D005023C4AD0050305': 'SB na opr 3_3',
    'RWS01_MONICA_00D005022415D0050005': 'SB tussen afop 2',
    'RWS01_MONICA_00D005022415D0050009': 'SB tussen afop 2_2',
    'RWS01_MONICA_00D005020442D0050005': 'SB na opr 2',
    'RWS01_MONICA_00D005020442D0050009': 'SB na opr 2_2',
    'RWS01_MONICA_00D005020442D007000B': 'NB voor afr 2',
    'RWS01_MONICA_00D005020442D0070007': 'NB voor afr 2_2',
    'RWS01_MONICA_00D005021841D007000B': 'NB tussen afop 2',
    'RWS01_MONICA_00D005021841D0070007': 'NB tussen afop 2_2',
    'RWS01_MONICA_00D005023047D007000B': 'NB na opr 2',
    'RWS01_MONICA_00D005023047D0070007': 'NB na opr 2_2',
    'RWS01_MONICA_00D005023047D0070307': 'NB na opr 2_3',
    'RWS01_MONICA_00D005024C43D007000B': 'NB tussen afop 3',
    'RWS01_MONICA_00D005024C43D0070007': 'NB tussen afop 3_2',
    'RWS01_MONICA_00D005026041D007000B': 'NB na opr 3',
    'RWS01_MONICA_00D005026041D0070007': 'NB na opr 3_2'
}
df = df.rename(columns=rename)

# Calculate ingaand values
df['SB ingaand 2'] = (df['SB na opr 3'] + df['SB na opr 3_2'] + df['SB na opr 3_3']) - (df['SB tussen afop 2'] + df['SB tussen afop 2_2'])
df['SB ingaand 3'] = (df['SB voor afr 3'] + df['SB voor afr 3_2']) - (df['SB tussen afop 3'] + df['SB tussen afop 3_2'])
df['NB ingaand 2'] = (df['NB voor afr 2'] + df['NB voor afr 2_2']) - (df['NB tussen afop 2'] + df['NB tussen afop 2_2'])
df['NB ingaand 3'] = (df['NB na opr 2'] + df['NB na opr 2_2'] + df['NB na opr 2_3']) - (df['NB tussen afop 3'] + df['NB tussen afop 3_2'])
df['ingaand'] = df['SB ingaand 2'] + df['SB ingaand 3'] + df['NB ingaand 2'] + df['NB ingaand 3']

# Calculate uitgaand values
df['SB uitgaand 3'] = (df['SB na opr 3'] + df['SB na opr 3_2'] + df['SB na opr 3_3']) - (df['SB tussen afop 3'] + df['SB tussen afop 3_2'])
df['SB uitgaand 2'] = (df['SB na opr 2'] + df['SB na opr 2_2']) - (df['SB tussen afop 2'] + df['SB tussen afop 2_2'])
df['NB uitgaand 2'] = (df['NB na opr 2'] + df['NB na opr 2_2'] + df['NB na opr 2_3']) - (df['NB tussen afop 2'] + df['NB tussen afop 2_2'])
df['NB uitgaand 3'] = (df['NB na opr 3'] + df['NB na opr 3_2']) - (df['NB tussen afop 3'] + df['NB tussen afop 3_2'])
df['uitgaand'] = df['SB uitgaand 2'] + df['SB uitgaand 3'] + df['NB uitgaand 2'] + df['NB uitgaand 3']

# Streamlit app
st.title('Traffic Flow Analysis - Ingaand and Uitgaand')

# Convert index to datetime
df.index = pd.to_datetime(df.index)

# Date range selector
min_date = df.index.min().date()
max_date = df.index.max().date()
start_date = st.date_input('Start date', min_date)
end_date = st.date_input('End date', max_date)

# Convert to datetime
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filter data based on date range
mask = (df.index >= start_date) & (df.index <= end_date)
filtered_df = df.loc[mask]

# Group by options
group_by = st.selectbox('Group by', ['Day', 'Week', 'Month', 'Weekday'])

if group_by == 'Day':
    grouped_df = filtered_df
elif group_by == 'Week':
    grouped_df = filtered_df.resample('W').sum()
elif group_by == 'Month':
    grouped_df = filtered_df.resample('M').sum()
elif group_by == 'Weekday':
    grouped_df = filtered_df.groupby(filtered_df.index.weekday).sum()
    grouped_df.index = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

# Calculate relative intensity (max value = 100%) for both ingaand and uitgaand
max_intensity = max(grouped_df['ingaand'].max(), grouped_df['uitgaand'].max())
grouped_df['relative_intensity_ingaand'] = (grouped_df['ingaand'] / max_intensity) * 100
grouped_df['relative_intensity_uitgaand'] = (grouped_df['uitgaand'] / max_intensity) * 100

# Checkbox for switching between relative and absolute values
use_relative_values = st.checkbox('Use Relative Values', value=True)

# Create plot
fig1 = go.Figure()

# Add bar traces for intensity
if use_relative_values:
    fig1.add_trace(go.Bar(x=grouped_df.index, y=grouped_df['relative_intensity_ingaand'], name='Ingaand'))
    fig1.add_trace(go.Bar(x=grouped_df.index, y=grouped_df['relative_intensity_uitgaand'], name='Uitgaand'))
    y_axis_title = 'Relative Intensity (%)'
else:
    fig1.add_trace(go.Bar(x=grouped_df.index, y=grouped_df['ingaand'], name='Ingaand'))
    fig1.add_trace(go.Bar(x=grouped_df.index, y=grouped_df['uitgaand'], name='Uitgaand'))
    y_axis_title = 'Absolute Intensity'

# Update layout
fig1.update_layout(title=f'{"Relative" if use_relative_values else "Absolute"} Traffic Flow ({group_by})',
                  xaxis_title='Date' if group_by != 'Weekday' else 'Day of Week',
                  yaxis_title=y_axis_title,
                  legend_title='Traffic Type',
                  yaxis=dict(range=[0, 100]) if use_relative_values else dict(),
                  barmode='group')  # Group bars side by side

# Display the plot
st.plotly_chart(fig1)

# Display raw data
if st.checkbox('Show raw data'):
    if use_relative_values:
        st.write(grouped_df[['ingaand', 'uitgaand', 'relative_intensity_ingaand', 'relative_intensity_uitgaand']])
    else:
        st.write(grouped_df[['ingaand', 'uitgaand']])

# New plot for average intensity per hour for selected weekday
st.subheader('Average Intensity per Hour for Selected Weekday')

# Prepare data for hourly weekday plot
filtered_df['hour'] = filtered_df.index.hour
filtered_df['weekday'] = filtered_df.index.weekday

# Dropdown for weekday selection
weekday_map = {0: 'Monday', 1: 'Tuesday', 2: 'Wednesday', 3: 'Thursday', 4: 'Friday', 5: 'Saturday', 6: 'Sunday'}
selected_weekday = st.selectbox('Select Weekday', list(weekday_map.values()))

# Filter data for selected weekday
selected_weekday_data = filtered_df[filtered_df['weekday'] == list(weekday_map.keys())[list(weekday_map.values()).index(selected_weekday)]]

# Calculate average intensity per hour for selected weekday for both traffic types
hourly_avg_ingaand = selected_weekday_data.groupby('hour')['ingaand'].mean()
hourly_avg_uitgaand = selected_weekday_data.groupby('hour')['uitgaand'].mean()

# Calculate relative intensity (max value = 100%) for both traffic types
max_hourly_intensity = max(hourly_avg_ingaand.max(), hourly_avg_uitgaand.max())
hourly_relative_intensity_ingaand = (hourly_avg_ingaand / max_hourly_intensity) * 100
hourly_relative_intensity_uitgaand = (hourly_avg_uitgaand / max_hourly_intensity) * 100

# Checkbox for switching between relative and absolute values for hourly plot
use_relative_values_hourly = st.checkbox('Use Relative Values for Hourly Plot', value=True)

# Create bar plot for selected weekday showing both traffic types
fig2 = go.Figure()

if use_relative_values_hourly:
    fig2.add_trace(go.Bar(x=[f"{i:02d}:00" for i in range(24)], 
                          y=hourly_relative_intensity_ingaand, 
                          name='Ingaand',
                          marker_color='blue'))
    fig2.add_trace(go.Bar(x=[f"{i:02d}:00" for i in range(24)], 
                          y=hourly_relative_intensity_uitgaand, 
                          name='Uitgaand',
                          marker_color='red'))
    y_axis_title_hourly = 'Relative Intensity (%)'
else:
    fig2.add_trace(go.Bar(x=[f"{i:02d}:00" for i in range(24)], 
                          y=hourly_avg_ingaand, 
                          name='Ingaand',
                          marker_color='blue'))
    fig2.add_trace(go.Bar(x=[f"{i:02d}:00" for i in range(24)], 
                          y=hourly_avg_uitgaand, 
                          name='Uitgaand',
                          marker_color='red'))
    y_axis_title_hourly = 'Absolute Intensity'

fig2.update_layout(title=f'Average {"Relative" if use_relative_values_hourly else "Absolute"} Intensity per Hour on {selected_weekday}',
                   xaxis_title='Hour of Day',
                   yaxis_title=y_axis_title_hourly,
                   yaxis=dict(range=[0, 100]) if use_relative_values_hourly else dict(),
                   barmode='group',  # Group bars side by side
                   legend_title='Traffic Type')

# Display the hourly plot
st.plotly_chart(fig2)

# Option to display raw hourly data
if st.checkbox('Show raw hourly data'):
    if use_relative_values_hourly:
        hourly_data = pd.DataFrame({
            'Hour': range(24),
            'Ingaand (%)': hourly_relative_intensity_ingaand,
            'Uitgaand (%)': hourly_relative_intensity_uitgaand
        })
    else:
        hourly_data = pd.DataFrame({
            'Hour': range(24),
            'Ingaand': hourly_avg_ingaand,
            'Uitgaand': hourly_avg_uitgaand
        })
    st.write(hourly_data)
