import streamlit as st
import numpy as np
import pandas as pd
import pymongo
import matplotlib.pyplot as plt


df = pd.read_csv("heartRate.csv")

df['datetime'] = pd.to_datetime(df['date'] + ' ' + df['time'], format='%Y-%m-%d %H:%M:%S')
df.set_index('datetime', inplace=True)

start_date = st.date_input("Select Start Date", df.index.min().date())
end_date = st.date_input("Select End Date", df.index.max().date())
filtered_df = df.loc[start_date:end_date]

fig, ax = plt.subplots()
ax.plot(filtered_df.index, filtered_df['heart_rate'])
ax.set_xlabel("Datetime")
ax.set_title("Heart Rate Over Time")
fig.set_size_inches(10, 6)
st.pyplot(fig)
