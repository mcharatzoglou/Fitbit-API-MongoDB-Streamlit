from export_to_dataframes.export_dataframes import MongoClientDataframes
from datetime import date

client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
)
startTime = date(year = 2023, month = 4, day = 20)
endTime =  date(year = 2023, month = 4, day = 20)
client.dataframe_heart_rate(start_date=startTime)
client.dataframe_heart_summary(start_date=startTime)
client.dataframe_heart_resting_heart_rate(start_date=startTime)