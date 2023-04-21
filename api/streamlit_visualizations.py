import streamlit as st
import numpy as np
import pandas as pd
import pymongo
import matplotlib.pyplot as plt


df = pd.read_csv("heartRate.csv")

df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S')
df.set_index('datetime', inplace=True)

# Create Streamlit picker widgets 
start_date = st.date_input("Select Start Date", df.index.min().date())
end_date = st.date_input("Select End Date", df.index.max().date())
start_time = st.time_input("Select Start Time", value=df.index.min().time())
end_time = st.time_input("Select End Time", value=df.index.max().time())

# Combine date and time into a single datetime object
start_datetime = pd.to_datetime(str(start_date) + ' ' + str(start_time))
end_datetime = pd.to_datetime(str(end_date) + ' ' + str(end_time))

# Filter the dataframe 
filtered_df = df.loc[start_datetime:end_datetime]

#create the plot
fig, ax = plt.subplots()
ax.plot(filtered_df.index, filtered_df['heart_rate'])
ax.set_xlabel("Time")
ax.set_ylabel("Heart Rate")
ax.set_title("Heart Rate Over Time")
ax.xaxis.set_major_formatter(plt.FixedFormatter(filtered_df.index.strftime('%Y-%m-%d %H:%M')))
ax.tick_params(axis='x', rotation=45) # Add this line to rotate the x-axis labels
st.pyplot(fig)