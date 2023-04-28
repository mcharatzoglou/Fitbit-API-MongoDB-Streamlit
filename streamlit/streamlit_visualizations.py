import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import sys
sys.path.append('../export_to_dataframes')
from export_dataframes import MongoClientDataframes


def plot_hr_ts():
    '''creates a plot of the heart rate time series for the user defined date range'''

    st.markdown("<h3 style='color: blue'>Heart Rate Time Series</h3>", unsafe_allow_html=True)

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date", 
                    value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                    key="date1")
    end_date = st.date_input("Select Ending Date",
                    value=dt.datetime.strptime("2023-03-28", "%Y-%m-%d"),
                    key="date2")

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_heart_rate(start_date, end_date)
    # Check if df is empty 
    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        # Combine date and time into one column
        filtered_df['datetime'] = pd.to_datetime(filtered_df['date'] + ' ' + filtered_df['time'], format='%Y-%m-%d %H:%M:%S')
        filtered_df.set_index('datetime', inplace=True)
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


def hr_boxplot():
    '''creates boxplot of heart rate for user defined date range'''

    st.markdown("<h3 style='color: green'>Heart Rate Boxplot</h3>", unsafe_allow_html=True)

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date", 
                    value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                     key="date3")
    end_date = st.date_input("Select Ending Date", 
                value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                key="date4")

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_heart_rate(start_date, end_date)

    # Check if selected_data is empty
    if filtered_df.empty:
        st.write("No data available for selected date range.")
    else:
        #create the plot
        fig, ax = plt.subplots()
        ax.boxplot(filtered_df["heart_rate"])
        ax.set_title(f"Heart Rate from {start_date} to {end_date}")
        ax.set_ylabel("Heart Rate values")
        st.pyplot(fig)



def hr_pie_chart():
    '''creates a pie chart plot wrt heart rate zones and corresponding avg duration
    for the user defined date range'''

    st.markdown("<h3 style='color: orange'>Heart Rate Zone Trends</h3>", unsafe_allow_html=True)

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date", 
                value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                key="date5")
    end_date = st.date_input("Select Ending Date", 
                value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                key="date6")

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_heart_summary(start_date, end_date)

    #convert column of date to datetime values
    #df["date"] = pd.to_datetime(df["date"])
    #df["date"] = df["date"].dt.date
    #filtered_df.set_index('date', inplace=True)

    if filtered_df.empty:
        st.write("No data available for selected date range.")
    else:
        #create the plot
        fig, ax = plt.subplots()
        names = set(filtered_df["name"].values)
        #get total number of minutes
        total_dur = np.sum(filtered_df["minutes"].values)
        zone_dict = dict() #dict zone name: average duration in minutes
        for name in names:
            #get a df for each zone
            zone_df = filtered_df[filtered_df["name"]==name]
            dur = filtered_df["minutes"].values
            zone_dict[name]=(np.sum(zone_df["minutes"].values)/total_dur)*100
        zone_colors = dict()
        zone_colors["Out of Range"] = 'red'
        zone_colors["Fat Burn"] = "green"
        zone_colors["Cardio"] = "blue"
        zone_colors["Peak"] = "yellow"
        ax.pie(zone_dict.values(), labels=None, 
               colors=[zone_colors[z] for z in names])
        legend_labels = [f'{z} ({p:.1f}%)' for z, p in zip(zone_dict.keys(), zone_dict.values())]
        ax.legend(legend_labels, loc='best', bbox_to_anchor=(1.0, 0.5)) 
        ax.set_title(f"Heart Rate Zone Distribution from {start_date} to {end_date}")
        st.pyplot(fig)
      

def calorie_bar():
    '''creates a pie chart plot wrt heart rate zones and corresponding avg duration
    for the user defined date range'''

    st.markdown("<h3 style='color: yellow'>Calories Burnt (Daily Average)</h3>", unsafe_allow_html=True)

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date", 
                value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                key="date7")
    end_date = st.date_input("Select Ending Date", 
                value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                key="date8")

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_heart_summary(start_date, end_date)

    if filtered_df.empty:
        st.write("No data available for selected date range.")
    else:
        #create the plot
        names = set(filtered_df["name"].values)
        calorie_dict = dict() #dict zone name: average duration in minutes
        for name in names:
            #get a df for each zone
            zone_df = filtered_df[filtered_df["name"]==name]
            calorie_dict[name]=np.mean(zone_df["caloriesOut"].values)
        fig, ax = plt.subplots(figsize = (8, 5))
        ax.bar(calorie_dict.keys(), calorie_dict.values())
        ax.set_xlabel('Heart Rate Zone')
        ax.set_ylabel('Calories Burnt')
        ax.set_title(f"Calories Burnt in Each Heart Rate Zone from {start_date} to {end_date} (Daily Average)")        
        st.pyplot(fig)


def rhr_boxplot():
    '''creates boxplot of resting heart rate for user defined date range'''

    st.markdown("<h3 style='color: green'>Resting Heart Rate Boxplot</h3>", unsafe_allow_html=True)

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date", 
                    value=dt.datetime.strptime("2023-03-28", "%Y-%m-%d"),
                     key="date9")
    end_date = st.date_input("Select Ending Date", 
                value=dt.datetime.strptime("2023-03-29", "%Y-%m-%d"),
                key="date10")

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_heart_resting_heart_rate(start_date, end_date)
    print(filtered_df)
    # Check if selected_data is empty
    if filtered_df.empty:
        st.write("No data available for selected date range.")
    else:
        #create the plot
        fig, ax = plt.subplots()
        ax.boxplot(filtered_df["restingHeartRate"])
        ax.set_title(f"Resting Heart Rate from {start_date} to {end_date}")
        ax.set_ylabel("Resting Heart Rate values")
        st.pyplot(fig)


def plot_hrv_ts():
    '''creates a plot of the heart rate variabiility time series
    for the user defined date range'''

    st.markdown("<h3 style='color: blue'>Heart Rate Variability Time Series</h3>", 
                unsafe_allow_html=True)

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date", 
                    value=dt.datetime.strptime("2023-04-21", "%Y-%m-%d"),
                    key="date11")
    end_date = st.date_input("Select Ending Date",
                    value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                    key="date12")

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_hrv(start_date, end_date)
    # Check if df is empty 
    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        #create the plot
        fig, ax = plt.subplots()
        ax.plot(filtered_df["date"], 
                filtered_df['daily_rmssd'], label="Daily RMSSD",
                  linewidth=0.8)
        ax.plot(filtered_df["date"], 
                filtered_df['deep_rmssd'], label="Deep Sleep RMSSD",
                  linewidth=0.8)
        ax.set_xlabel("Time")
        ax.set_ylabel("Heart Rate Variability values")
        ax.set_title("Heart Rate Variability Over Time")   
        ax.tick_params(axis='x', rotation=45, labelsize=6) 
        ax.tick_params(axis='y', labelsize=6) 
        ax.legend()
        st.pyplot(fig)



container = st.container()
container.markdown("<h1 style='color: red'>My Fitbit data</h1>", unsafe_allow_html=True)


plot_hr_ts()
hr_boxplot()
hr_pie_chart()
calorie_bar()
rhr_boxplot()
plot_hrv_ts()


