import streamlit as st

# Create tabs using beta_container
tabs = ["Heart Rate", "Sleep"]
selected_tab = st.sidebar.radio("Select Tab", tabs)

# Display content based on selected tab
if selected_tab == "Heart Rate":
    df = pd.read_csv("heartRate.csv")

    df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S')
    df.set_index('datetime', inplace=True)

    st.title('My Fitbit data')
    st.markdown("### Heart Rate Data")
        
    # Create Streamlit picker widgets 
    start_date = st.date_input("Select Start Date", df.index.min().date())
    start_time = st.time_input("Select Start Time", value=df.index.min().time())
    end_date = st.date_input("Select End Date", df.index.max().date())
    end_time = st.time_input("Select End Time", value=df.index.max().time())

    # Combine date and time into a single datetime object
    start_datetime = pd.to_datetime(str(start_date) + ' ' + str(start_time))
    end_datetime = pd.to_datetime(str(end_date) + ' ' + str(end_time))

    # Filter the dataframe 
    filtered_df = df.loc[start_datetime:end_datetime]

    #create the plot
    fig, ax = plt.subplots()
    ax.plot(filtered_df.index, filtered_df['heart_rate'],linewidth=0.4)
    ax.set_xlabel("Time")
    ax.set_ylabel("Heart Rate")
    ax.set_title("Heart Rate Over Time")
    date_fmt = "%m/%d/%Y %H:%M"
    date_formatter = mdates.DateFormatter(date_fmt)
    ax.xaxis.set_major_formatter(date_formatter)
    ax.tick_params(axis='x', rotation=45, labelsize=6) 
    ax.tick_params(axis='y', labelsize=6) 


    st.pyplot(fig)

elif selected_tab == "Sleep":
    st.title("Sleep Visualization")
    # Import and display visualization from python file for Sleep
    import streamlit as st
    import numpy as np
    import pandas as pd
    # import pymongo
    import matplotlib.pyplot as plt

    df = pd.read_csv(
        r"C:\Users\sophi\PycharmProjects\2nd-Lab-Project-Fitbit-API-MongoDB-Streamlit\api\minutesStagesSleep.csv")

    df['datetime'] = pd.to_datetime(df['date'], format='%Y-%m-%d')

    # Set the datetime column as the index of the dataframe
    df.set_index('datetime', inplace=True)

    start_date = st.date_input("Select Start Date", df.index.min().date())
    end_date = st.date_input("Select End Date", df.index.max().date())

    # Create two Streamlit time picker widgets to allow users to select the start and end times of the range
    start_time = st.time_input("Select Start Time", value=df.index.min().time())
    end_time = st.time_input("Select End Time", value=df.index.max().time())

    # Combine the selected date and time into a single datetime object
    start_datetime = pd.to_datetime(str(start_date) + ' ' + str(start_time))
    end_datetime = pd.to_datetime(str(end_date) + ' ' + str(end_time))

    # Filter the dataframe based on the selected datetime range
    filtered_df = df.loc[start_datetime:end_datetime]

    '''
    #plot of total minutes asleep
    fig, ax = plt.subplots()
    ax.plot(filtered_df.index, filtered_df['totalMinutesAsleep'])
    ax.set_xlabel("Datetime")
    ax.set_title("Minutes of Sleep Over Time")
    fig.set_size_inches(10, 6)
    st.pyplot(fig)

    #plot of total time in bed
    fig, ax = plt.subplots()
    ax.plot(filtered_df.index, filtered_df['totalTimeInBed'])
    ax.set_xlabel("Datetime")
    ax.set_title("Minutes in bed Over Time")
    fig.set_size_inches(10, 6)
    st.pyplot(fig)
    '''

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(filtered_df.index, filtered_df['totalMinutesAsleep'], color='blue', label='Minutes of Sleep')
    ax.plot(filtered_df.index, filtered_df['totalTimeInBed'], color='orange', label='Minutes in Bed')

    ax.set_xlabel("Datetime")
    ax.set_ylabel("Minutes")
    ax.set_title("Sleep and Bed Time Over Time")
    ax.legend()

    st.pyplot(fig)


