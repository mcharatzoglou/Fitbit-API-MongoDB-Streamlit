import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import sys
sys.path.append(r'C:\Users\sophi\PycharmProjects\2nd-Lab-Project-Fitbit-API-MongoDB-Streamlit\export_to_dataframes')
from export_dataframes import MongoClientDataframes


#1 Plot sleep VS bedtime for a specific date range
def plot_slbed_ts():

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date",
                    value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                    key="date1")
    end_date = st.date_input("Select Ending Date",
                    value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                    key="date2")

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string= "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_sleep_metrics(start_date, end_date)
    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        filtered_df['datetime'] = pd.to_datetime(filtered_df['date'])
        filtered_df.set_index('datetime', inplace=True)
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.plot(filtered_df.index, filtered_df['minutesAsleep'], color='blue', label='Minutes of Sleep')
        ax.plot(filtered_df.index, filtered_df['timeInBed'], color='orange', label='Minutes in Bed')

        ax.set_xlabel("Datetime")
        ax.set_ylabel("Minutes")
        ax.set_title("Sleep and Bed Time Over Time")
        ax.legend()
        ax.tick_params(axis='x', rotation=45, labelsize=6)
        ax.tick_params(axis='y', labelsize=6)

        st.pyplot(fig)
st.title('Sleep VS Time in Bed comparison')
plot_slbed_ts()



#2 Plot pie chart of sleep stages for a given date
# create a list of dates to use in the date picker
def plot_sleep_stages(data, date):
    # filter the dataframe to include only the data for the specified date
    data = data[data['date'] == date]
    if data.empty:
        st.write("No data available for selected date.")
    else:
        # create the pie chart
        fig, ax = plt.subplots(figsize=(6, 6))
        ax.pie(data['totalMinutesAsleep'], labels=data['stage'], autopct='%1.1f%%', startangle=90)
        ax.set_title(f'Sleep stages for {date}')
        st.pyplot(fig)

st.title('Sleep Summary Pie Chart')

# add a date picker to select the date to display
date = st.date_input("Select a date",
                     value=dt.datetime.strptime("2023-04-27", "%Y-%m-%d"),
                     key="date")

# create a MongoDB client to connect to the database
client = MongoClientDataframes(
    connection_string="mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
)

# retrieve the sleep summary data for the selected date
data = client.dataframe_sleep_summary(date)

# generate the pie chart for the selected date
plot_sleep_stages(data, date.strftime("%Y-%m-%d"))



#3 Plot Average Sleep Duration Over Time
def plot_sleep_duration():
    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date",
                               value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                               key="date5")
    end_date = st.date_input("Select Ending Date",
                             value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                             key="date6")

    # get data from MongoDB as dataframe
    client = MongoClientDataframes(
        connection_string="mongodb://localhost:27017/",
        database="local",
        collection="fitbit",
    )

    filtered_df = client.dataframe_sleep_metrics(start_date, end_date)
    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        # groupby date and calculate mean of sleep duration
        filtered_df = filtered_df.groupby("date").mean()["minutesAsleep"].reset_index()

        # Create the bar plot
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.bar(filtered_df["date"], filtered_df["minutesAsleep"], color='pink')
        ax.set_xlabel('Date')
        ax.set_ylabel('Sleep Duration (minutes)')
        ax.set_title('Average Sleep Duration over Time')
        ax.tick_params(axis='x', rotation=45, labelsize=6)
        ax.tick_params(axis='y', labelsize=6)
        st.pyplot(fig)

st.title("Average Sleep Duration Over Time")
# Generate the bar plot
plot_sleep_duration()



#4 Plot Duration VS Efficiency for comparison
def plot_duration_vs_efficiency():
    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date",
                               value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                               key="date7")
    end_date = st.date_input("Select Ending Date",
                             value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                             key="date8")

    # get data from MongoDB as dataframe
    client = MongoClientDataframes(
        connection_string="mongodb://localhost:27017/",
        database="local",
        collection="fitbit",
    )
    filtered_df = client.dataframe_sleep_metrics(start_date, end_date)

    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        # Create the bar plot
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax2 = ax1.twinx()

        ax1.set_xlabel('Date')
        ax1.set_ylabel('Sleep Duration (minutes)')
        ax2.set_ylabel('Sleep Efficiency (%)')
        ax1.set_title('Sleep Duration and Efficiency over Time')

        # groupby date and calculate mean of sleep duration and efficiency
        filtered_df = filtered_df.groupby("date").mean()[["minutesAsleep", "efficiency"]].reset_index()

        ax1.bar(filtered_df["date"], filtered_df["minutesAsleep"], color="blue", alpha=0.5, label="Duration")
        ax2.plot(filtered_df["date"], filtered_df["efficiency"], color="red", marker="o", label="Efficiency")
        ax1.tick_params(axis='x', rotation=45, labelsize=6)
        ax1.tick_params(axis='y', labelsize=6)
        ax2.tick_params(axis='y', labelsize=6)
        ax1.legend(loc="upper left")
        ax2.legend(loc="upper right")

        st.pyplot(fig)


st.title("Sleep Duration and Efficiency Over Time")
# Generate the bar plot
plot_duration_vs_efficiency()



#5 Plot minutes Asleep and Awake over Time
def plot_sleep_line_chart():
    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date",
                               value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                               key="date9")
    end_date = st.date_input("Select Ending Date",
                             value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                             key="date10")

    # Get data from MongoDB as dataframe
    client = MongoClientDataframes(
        connection_string="mongodb://localhost:27017/",
        database="local",
        collection="fitbit",
    )
    filtered_df = client.dataframe_sleep_metrics(start_date, end_date)

    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        # Group by date and calculate mean of sleep metrics
        filtered_df = filtered_df.groupby("date").mean()[["minutesAsleep", "minutesAwake"]].reset_index()

        # Create line chart
        fig, ax = plt.subplots(figsize=(10, 6))

        ax.set_xlabel('Date')
        ax.set_ylabel('Minutes')
        ax.set_title('Minutes Asleep and Awake over Time')

        ax.plot(filtered_df["date"], filtered_df["minutesAsleep"], color="blue", marker="o", label="Minutes Asleep")
        ax.plot(filtered_df["date"], filtered_df["minutesAwake"], color="red", marker="o", label="Minutes Awake")
        ax.tick_params(axis='x', rotation=45, labelsize=6)
        ax.tick_params(axis='y', labelsize=6)
        ax.legend()

        st.pyplot(fig)

st.title("Minutes Asleep and Awake over Time")
# Generate the line chart
plot_sleep_line_chart()



# 6 histogram of the distribution of sleep start times for each hour of the day for a specific date range
# Function to plot sleep start and end time histograms
def plot_sleep_timing():
    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date",
                               value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                               key="date11")
    end_date = st.date_input("Select Ending Date",
                             value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                             key="date12")

    # get data from MongoDB as dataframe
    client = MongoClientDataframes(
        connection_string="mongodb://localhost:27017/",
        database="local",
        collection="fitbit",
    )
    filtered_df = client.dataframe_sleep_metrics(start_date, end_date)

    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        # format startTime and endTime columns as datetime objects
        filtered_df["startTime"] = pd.to_datetime(filtered_df["startTime"])
        filtered_df["endTime"] = pd.to_datetime(filtered_df["endTime"])

        # Create the histogram
        fig, ax1 = plt.subplots(figsize=(10, 6))

        ax1.set_xlabel('Hour of Day')
        ax1.set_ylabel('Number of Days')
        ax1.set_title('Sleep Timing Histogram')

        ax1.hist(filtered_df["startTime"].dt.hour, bins=24, color="blue", alpha=0.5, label="Bedtime")
        ax1.hist(filtered_df["endTime"].dt.hour, bins=24, color="green", alpha=0.5, label="Wake-up time")

        # Set x-axis tick positions to every hour
        ax1.set_xticks(range(0, 24))
        ax1.legend()

        st.pyplot(fig)

st.title("Average Sleep Timing Analysis")
# Generate the histogram
plot_sleep_timing()