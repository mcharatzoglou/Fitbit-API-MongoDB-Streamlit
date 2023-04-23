import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

container = st.container()
container.markdown("<h1 style='color: red'>My Fitbit data</h1>", unsafe_allow_html=True)


st.markdown("<h3 style='color: blue'>Heart Rate Time Series</h3>", unsafe_allow_html=True)

df = pd.read_csv("heartRate.csv")

df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S')
df.set_index('datetime', inplace=True)
        
# Create Streamlit picker widgets 
start_date = st.date_input("Select Start Date", df.index.min().date())
start_time = st.time_input("Select Start Time", value=df.index.min().time())
end_date = st.date_input("Select End Date", df.index.max().date())
end_time = st.time_input("Select End Time", value=df.index.max().time())

# Combine date and time into a single datetime object
start_datetime = pd.to_datetime(str(start_date) + ' ' + str(start_time))
end_datetime = pd.to_datetime(str(end_date) + ' ' + str(end_time))

# Filter data
filtered_df = df.loc[start_datetime:end_datetime]

# Check if df is empty  
if filtered_df.empty:
    st.write("No data available for selected date.")
else:
    #create the plot
    fig, ax = plt.subplots()
    ax.plot(filtered_df.index, filtered_df['heart_rate'],linewidth=0.4)
    ax.set_xlabel("Time")
    ax.set_ylabel("Heart Rate values")
    ax.set_title("Heart Rate Over Time")
    date_fmt = "%Y/%m/%d %H:%M"
    date_formatter = mdates.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)
    ax.tick_params(axis='x', rotation=45, labelsize=6) 
    ax.tick_params(axis='y', labelsize=6) 
    st.pyplot(fig)




#create boxplot of heart rate for selected date
st.markdown("<h3 style='color: blue'>Heart Rate Boxplot</h3>", unsafe_allow_html=True)

df = pd.read_csv("heartRate.csv")
#convert column of date to datetime values
df["date"] = pd.to_datetime(df["date"])
df["date"] = df["date"].dt.date

# Create Streamlit picker widgets 
specified_date = st.date_input("Select Specific Date", df["date"].min())

# Filter data
filtered_df = df[df["date"] == specified_date]

# Check if selected_data is empty
if filtered_df.empty:
    st.write("No data available for selected date.")
else:
    #create the plot
    fig, ax = plt.subplots()
    ax.boxplot(filtered_df["heart_rate"])
    ax.set_title(f"Heart Rate for {specified_date}")
    ax.set_ylabel("Heart Rate values")
    st.pyplot(fig)
