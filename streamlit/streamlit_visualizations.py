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
    '''creates boxplot of heart rate for user defined date'''

    st.markdown("<h3 style='color: green'>Daily Heart Rate Boxplot</h3>", unsafe_allow_html=True)

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Specific Date", 
                    value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                     key="date3")
    end_date = start_date

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_heart_rate(start_date, end_date)

    # Check if selected_data is empty
    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        #create the plot
        fig, ax = plt.subplots()
        ax.boxplot(filtered_df["heart_rate"])
        ax.set_title(f"Heart Rate for {start_date}")
        ax.set_ylabel("Heart Rate values")
        st.pyplot(fig)


def hr_pie_chart():
    '''creates a pie chart plot wrt heart rate zones and corresponding duration
    for the user defined date'''

    st.markdown("<h3 style='color: orange'>Daily Distribution of Heart Rate Zones</h3>", unsafe_allow_html=True)

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Specific Date", 
                value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                key="date4")
    end_date = start_date

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_heart_summary(start_date, end_date)

    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        #create the plot
        fig, ax = plt.subplots()
        names = filtered_df["name"].values
        dur = filtered_df["minutes"].values
        total_dur = np.sum(dur)
        percentages = [d/total_dur*100 for d in dur]
        zone_colors = dict()
        zone_colors["Out of Range"] = 'red'
        zone_colors["Fat Burn"] = "green"
        zone_colors["Cardio"] = "blue"
        zone_colors["Peak"] = "yellow"
        ax.pie(percentages, labels=None, 
               autopct=None, colors=[zone_colors[z] for z in names])
        # Create a legend
        legend_labels = [f'{z} ({p:.1f}%)' for z, p in zip(names, percentages)]
        ax.legend(legend_labels, loc='best', bbox_to_anchor=(1.0, 0.5))        
        ax.set_title(f"Heart Rate Zone Distribution for {start_date}")
        st.pyplot(fig)


def hr_pie_chart_avg():
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
    '''creates a bar plot wrt heart rate zones and corresponding calories burnt
    for the user defined date'''

    st.markdown("<h3 style='color: yellow'>Daily Heart Rate Zone Calories</h3>", unsafe_allow_html=True)

    start_date = st.date_input("Select Specific Date", 
                value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                key="date7")
    end_date = start_date

    #get data from MongoDB as dataframe
    client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    )
    filtered_df = client.dataframe_heart_summary(start_date, end_date)

    if filtered_df.empty:
        st.write("No data available for selected date.")
    else:
        #create the plot
        names = filtered_df["name"].values
        cal = filtered_df["caloriesOut"].values
        final_names, final_cal = [], []
        #plot only the zones with calories>0
        '''for i in range(len(names)):
            if cal[i]>0:
                final_names.append(names[i])
                final_cal.append(cal[i])
        if len(final_names)>2:
            figsize = (8, 5)
        else:
            figsize = (1, 5)
        fig, ax = plt.subplots(figsize=figsize)
        ax.bar(final_names, final_cal)'''
        fig, ax = plt.subplots(figsize = (8, 5))
        ax.bar(names, cal)
        ax.set_xlabel('Heart Rate Zone')
        ax.set_ylabel('Calories Burnt')
        ax.set_title(f"Calories Burnt in Each Heart Rate Zone for {start_date}")
        #plt.xticks(rotation=45, ha='right')
        st.pyplot(fig)


def calorie_bar_avg():
    '''creates a pie chart plot wrt heart rate zones and corresponding avg duration
    for the user defined date range'''

    st.markdown("<h3 style='color: yellow'>Calories Burnt (Daily Average)</h3>", unsafe_allow_html=True)

    # Create Streamlit picker widgets
    start_date = st.date_input("Select Starting Date", 
                value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                key="date8")
    end_date = st.date_input("Select Ending Date", 
                value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                key="date9")

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


container = st.container()
container.markdown("<h1 style='color: red'>My Fitbit data</h1>", unsafe_allow_html=True)


plot_hr_ts()
hr_boxplot()
hr_pie_chart()
hr_pie_chart_avg()
calorie_bar()
calorie_bar_avg()


