import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import datetime as dt
import sys
import os
import pickle
sys.path.append('../export_to_dataframes')
from export_dataframes import MongoClientDataframes

#create a container
container = st.container()

# Create tabs using container
tabs = ["Heart Rate & Heart Rate Variability", "Sleep"]
with container:
    selected_tab = st.sidebar.radio("Select Tab", tabs)

# Display content based on selected tab
with container:
    container.markdown("<h1 style='color: red'>My Fitbit data</h1>", unsafe_allow_html=True)

    if selected_tab == "Heart Rate & Heart Rate Variability":

        def plot_hr_ts():
            '''Plot 1: creates a plot of the heart rate time series for the user defined date range'''

            st.markdown("<h3 style='color: blue'>Heart Rate Time Series</h3>", 
                        unsafe_allow_html=True)

            # Create Streamlit picker widgets
            start_date = st.date_input("Select Starting Date",
                                    value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                                    key="date1")
            end_date = st.date_input("Select Ending Date",
                                    value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                                    key="date2")

            # get data from MongoDB as dataframe
            client = MongoClientDataframes(
                connection_string="mongodb://localhost:27017/",
                database="local",
                collection="fitbit",
            )
            filtered_df = client.dataframe_heart_rate(start_date, end_date)
            # Check if df is empty
            if filtered_df.empty:
                st.write("No data available for selected date.")
            else:
                # Combine date and time into one column
                filtered_df['datetime'] = pd.to_datetime(filtered_df['date'] + ' ' + filtered_df['time'],
                                                        format='%Y-%m-%d %H:%M:%S')
                filtered_df.set_index('datetime', inplace=True)
                # create the plot
                fig, ax = plt.subplots()
                ax.plot(filtered_df.index, filtered_df['heart_rate'], linewidth=0.4)
                ax.set_xlabel("Time")
                ax.set_ylabel("Heart Rate values")
                ax.set_title("Heart Rate Over Time")
                date_fmt = "%Y/%m/%d %H:%M"
                date_formatter = mdates.DateFormatter(date_fmt)
                ax.xaxis.set_major_formatter(date_formatter)
                ax.tick_params(axis='x', rotation=45, labelsize=6)
                ax.tick_params(axis='y', labelsize=6)
                st.pyplot(fig)
                plt.close(fig)


        def hr_boxplot():
            '''Plot 2: creates boxplot of heart rate for user defined date range'''

            st.markdown("<h3 style='color: green'>Heart Rate Boxplot</h3>", 
                        unsafe_allow_html=True)

            # Create Streamlit picker widgets
            start_date = st.date_input("Select Starting Date",
                                    value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                                    key="date3")
            end_date = st.date_input("Select Ending Date",
                                    value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                                    key="date4")

            # get data from MongoDB as dataframe
            client = MongoClientDataframes(
                connection_string="mongodb://localhost:27017/",
                database="local",
                collection="fitbit",
            )
            filtered_df = client.dataframe_heart_rate(start_date, end_date)

            # Check if selected_data is empty
            if filtered_df.empty:
                st.write("No data available for selected date range.")
            else:
                # create the plot
                fig, ax = plt.subplots()
                ax.boxplot(filtered_df["heart_rate"])
                ax.set_title(f"Heart Rate from {start_date} to {end_date}")
                ax.set_ylabel("Heart Rate values")
                st.pyplot(fig)
                plt.close(fig)


        def hr_pie_chart():
            '''Plot 3: creates a pie chart plot wrt heart rate zones and corresponding avg duration
            for the user defined date range'''

            st.markdown("<h3 style='color: orange'>Heart Rate Zone Trends</h3>", 
                        unsafe_allow_html=True)

            # Create Streamlit picker widgets
            start_date = st.date_input("Select Starting Date",
                                    value=dt.datetime.strptime("2023-04-18", "%Y-%m-%d"),
                                    key="date5")
            end_date = st.date_input("Select Ending Date",
                                    value=dt.datetime.strptime("2023-04-18", "%Y-%m-%d"),
                                    key="date6")

            # get data from MongoDB as dataframe
            client = MongoClientDataframes(
                connection_string="mongodb://localhost:27017/",
                database="local",
                collection="fitbit",
            )
            filtered_df = client.dataframe_heart_summary(start_date, end_date)

            if filtered_df.empty:
                st.write("No data available for selected date range.")
            else:
                # create the plot
                fig, ax = plt.subplots()
                names = set(filtered_df["name"].values)
                # get total number of minutes
                total_dur = np.sum(filtered_df["minutes"].values)
                zone_dict = dict()  # dict zone name: average duration in minutes
                for name in names:
                    # get a df for each zone
                    zone_df = filtered_df[filtered_df["name"] == name]
                    dur = filtered_df["minutes"].values
                    zone_dict[name] = (np.sum(zone_df["minutes"].values) / total_dur) * 100
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
                plt.close(fig)


        def calorie_bar():
            '''Plot 4: creates a pie chart plot wrt heart rate zones and corresponding avg duration
            for the user defined date range'''

            st.markdown("<h3 style='color: magenta'>Calories Burnt (Daily Average)</h3>", 
                        unsafe_allow_html=True)

            # Create Streamlit picker widgets
            start_date = st.date_input("Select Starting Date",
                                    value=dt.datetime.strptime("2023-04-18", "%Y-%m-%d"),
                                    key="date7")
            end_date = st.date_input("Select Ending Date",
                                    value=dt.datetime.strptime("2023-04-18", "%Y-%m-%d"),
                                    key="date8")

            # get data from MongoDB as dataframe
            client = MongoClientDataframes(
                connection_string="mongodb://localhost:27017/",
                database="local",
                collection="fitbit",
            )
            filtered_df = client.dataframe_heart_summary(start_date, end_date)

            if filtered_df.empty:
                st.write("No data available for selected date range.")
            else:
                # create the plot
                names = set(filtered_df["name"].values)
                calorie_dict = dict()  # dict zone name: average calories burnt
                for name in names:
                    # get a df for each zone
                    zone_df = filtered_df[filtered_df["name"] == name]
                    calorie_dict[name] = np.mean(zone_df["caloriesOut"].values)
                fig, ax = plt.subplots(figsize=(8, 5))
                ax.bar(calorie_dict.keys(), calorie_dict.values())
                ax.set_xlabel('Heart Rate Zone')
                ax.set_ylabel('Calories')
                ax.set_title(f"Calories Burnt from {start_date} to {end_date} (Daily Average)")
                st.pyplot(fig)
                plt.close(fig)


        def rhr_boxplot():
            '''Plot 5: creates boxplot of resting heart rate for user defined date range'''

            st.markdown("<h3 style='color: green'>Resting Heart Rate Boxplot</h3>", 
                        unsafe_allow_html=True)

            # Create Streamlit picker widgets
            start_date = st.date_input("Select Starting Date",
                                    value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                                    key="date9")
            end_date = st.date_input("Select Ending Date",
                                    value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                                    key="date10")

            # get data from MongoDB as dataframe
            client = MongoClientDataframes(
                connection_string="mongodb://localhost:27017/",
                database="local",
                collection="fitbit",
            )
            filtered_df = client.dataframe_heart_resting_heart_rate(start_date, end_date)
            # Check if selected_data is empty
            if filtered_df.empty:
                st.write("No data available for selected date range.")
            else:
                # create the plot
                fig, ax = plt.subplots()
                ax.boxplot(filtered_df["restingHeartRate"])
                ax.set_title(f"Resting Heart Rate from {start_date} to {end_date}")
                ax.set_ylabel("Resting Heart Rate values")
                st.pyplot(fig)
                plt.close(fig)


        def plot_hrv_ts():
            '''Plot 6: creates a plot of the heart rate variabiility time series
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

            # get data from MongoDB as dataframe
            client = MongoClientDataframes(
                connection_string="mongodb://localhost:27017/",
                database="local",
                collection="fitbit",
            )
            filtered_df = client.dataframe_hrv(start_date, end_date)
            # Check if df is empty
            if filtered_df.empty:
                st.write("No data available for selected date.")
            else:
                # create the plot
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
                plt.close(fig)

        
        def predict_next_hour():
            '''make predictions for the average heart rate of the next hour'''

            st.markdown("<h3 style='color: green'>Heart Rate: Next Hour Prediction</h3>", unsafe_allow_html=True)

            # Create Streamlit picker widgets
            start_date = st.date_input("Select Date",
                                    value=dt.datetime.strptime("2023-04-02", "%Y-%m-%d"),
                                    key="date13")
            end_date = start_date
            end_time = st.time_input("Select Time",
                                    value=dt.datetime.strptime("01:00:00", "%H:%M:%S"),
                                    key="time1")

            # get data from MongoDB as dataframe
            client = MongoClientDataframes(
                connection_string="mongodb://localhost:27017/",
                database="local",
                collection="fitbit",
            )
            df = client.dataframe_heart_rate(start_date, end_date)
            
            # Calculate the start time for the 60-minute window
            start_time = (dt.datetime.combine(start_date, end_time) - dt.timedelta(minutes=59)).time()
            # Check if df is empty
            if df.empty:
                st.write("No data available for selected date.")
            else:
                filtered_df = df[(df["time"]>=start_time.strftime('%H:%M:%S'))
                                &(df["time"]<=end_time.strftime('%H:%M:%S'))]
                if filtered_df.empty:     
                    st.write("No data available for selected date.")
                else:
                    data = filtered_df.heart_rate.values
                    X = []
                    # get mean values for each 5 minutes interval
                    for i in range(0,len(data),5):
                        X.append(np.mean(data[i:i+5]))
                    X = np.array(X)
                    if len(X)==12:
                        X = X.reshape(1, 12 , 1)
                        #load the model
                        parent_dir = os.path.abspath(os.path.join(os.getcwd(), '..'))
                        folder_path = os.path.join(parent_dir, 'machine_learning')    
                        with open(folder_path+'/lstm_model.p', 'rb') as f:
                            model = pickle.load(f)
                        #make prediction
                        pred = model.predict(X)
                        st.write(f"The average value for heart rate for the next hour is {pred[0][0]:.2f}")
                    else:
                        st.write("Sorry, no predictions can be done for this datetime.")

        plot_hr_ts()
        hr_boxplot()
        hr_pie_chart()
        calorie_bar()
        rhr_boxplot()
        plot_hrv_ts()
        predict_next_hour()


    elif selected_tab == "Sleep":
        # 1 Plot sleep VS bedtime for a specific date range
        def plot_slbed_ts():

            # Create Streamlit picker widgets
            start_date = st.date_input("Select Starting Date",
                                    value=dt.datetime.strptime("2023-03-27", "%Y-%m-%d"),
                                    key="date1")
            end_date = st.date_input("Select Ending Date",
                                    value=dt.datetime.strptime("2023-04-28", "%Y-%m-%d"),
                                    key="date2")

            # get data from MongoDB as dataframe
            client = MongoClientDataframes(
                connection_string="mongodb://localhost:27017/",
                database="local",
                collection="fitbit",
            )
            filtered_df = client.dataframe_sleep_metrics(start_date, end_date)
            if filtered_df.empty:
                st.write("No data available for the selected date.")
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
                plt.close(fig)


        #st.title('Sleep VS Time in Bed comparison')
        st.markdown("<h3 style='color: blue'>Sleep VS Time in Bed comparison</h3>", 
                    unsafe_allow_html=True)
        plot_slbed_ts()


        # 2 Plot pie chart of sleep stages for a given date
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
                plt.close(fig)


        #st.title('Sleep Summary Pie Chart')
        st.markdown("<h3 style='color: green'>Sleep Summary Pie Chart</h3>", 
                    unsafe_allow_html=True)

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


        # 3 Plot Average Sleep Duration Over Time
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
                plt.close(fig)


        #st.title("Average Sleep Duration Over Time")
        st.markdown("<h3 style='color: orange'>Average Sleep Duration Over Time</h3>", 
                    unsafe_allow_html=True)
        # Generate the bar plot
        plot_sleep_duration()


        # 4 Plot Duration VS Efficiency for comparison
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
                plt.close(fig)


        #st.title("Sleep Duration and Efficiency Over Time")
        st.markdown("<h3 style='color: magenta'>Sleep Duration and Efficiency Over Time</h3>", 
                    unsafe_allow_html=True)
        # Generate the bar plot
        plot_duration_vs_efficiency()


        # 5 Plot minutes Asleep and Awake over Time
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
                plt.close(fig)


        #st.title("Minutes Asleep and Awake over Time")
        st.markdown("<h3 style='color: green'>Minutes Asleep and Awake over Time</h3>", 
                    unsafe_allow_html=True)

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
                plt.close(fig)


        #st.title("Average Sleep Timing Analysis")
        st.markdown("<h3 style='color: blue'>Average Sleep Timing Analysis</h3>",
                        unsafe_allow_html=True)
        # Generate the histogram
        plot_sleep_timing()