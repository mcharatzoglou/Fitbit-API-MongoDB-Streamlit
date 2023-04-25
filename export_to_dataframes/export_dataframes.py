import pymongo
from datetime import date, datetime
import pandas as pd

class MongoClientDataframes:

    def __init__(self, connection_string, database, collection):
        # Connect to the MongoDB database and collection specified by the arguments
        try:
            self.mongo_client = pymongo.MongoClient(connection_string)
            self.db = self.mongo_client[database]
            self.collection = self.db[collection]
        except Exception as e:
            # If there is an error, set the connection variables to None and raise an exception
            self.mongo_client = None
            self.db = None
            self.collection = None
            raise Exception(e)

    def dataframe_heart_rate(self, start_date=None, end_date=None):
        # If start_date and end_date are not specified, set them to today's date
        start_date = start_date or datetime.now().date()
        end_date = end_date or datetime.now().date()

        # Convert the start and end dates to datetime objects
        start_datetime = datetime.combine(start_date, datetime.min.time())
        end_datetime = datetime.combine(end_date, datetime.max.time())

        # Format the start and end dates as strings in "YYYY-MM-DD" format
        date_format = "%Y-%m-%d"
        start_date_string = start_datetime.strftime(date_format)
        end_date_string = end_datetime.strftime(date_format)

        # Query the MongoDB collection for heart rate data between the start and end dates
        query = {
            "type": "heart", # Select documents with "type" equal to "heart"
            "date": { # Select documents where "date" is between the start and end dates
                "$gte": start_date_string, # Greater than or equal to start date
                "$lte": end_date_string  # Less than or equal to end date
            }
        }
        results = self.collection.find(query)

        # Extract heart rate data from the MongoDB documents and store it as a list of dictionaries
        data = [
            {
                'date': result['date'], # Date of the document
                'time': item['time'], # Time of the heart rate measurement
                'heart_rate': item['value'] # Heart rate value
            }
            for result in results
            for item in result['heartIntraday'] # Loop through the heart rate measurements for each document
        ]

        # Create a pandas dataframe from the list of dictionaries
        df = pd.DataFrame(data)

        # Save the dataframe to a CSV file with a descriptive file name
        filename = f"heart_rate_data_{start_date_string}_{end_date_string}.csv"
        df.to_csv(filename, index=False)

        # Return the pandas dataframe
        return df

# EXAMPLE CODE
client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
)
startTime = date(year = 2023, month = 4, day = 20)
endTime =  date(year = 2023, month = 4, day = 20)
client.dataframe_heart_rate(start_date=startTime)