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
        # filename = f"heart_rate_data_{start_date_string}_{end_date_string}.csv"
        # df.to_csv(filename, index=False)

        # Return the pandas dataframe
        return df

    def dataframe_heart_summary(self, start_date=None, end_date=None):
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
                'caloriesOut': item['caloriesOut'], # Number calories burned with the specified heart rate zone
                'max': item['max'], # Maximum range for the heart rate zone
                'min': item['min'], # Minimum range for the heart rate zone
                'minutes': item['minutes'], # Number minutes withing the specified heart rate zone
                'name': item['name'] # Name of the heart rate zone
            }
            for result in results
            for item in result['heartRateZones'] # Loop through the heart rate measurements for each document
        ]

        # Create a pandas dataframe from the list of dictionaries
        df = pd.DataFrame(data)

        # Save the dataframe to a CSV file with a descriptive file name
        # filename = f"heart_rate_summary_{start_date_string}_{end_date_string}.csv"
        # df.to_csv(filename, index=False)

        # Return the pandas dataframe
        return df

    def dataframe_heart_resting_heart_rate(self, start_date=None, end_date=None):
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
        data = []
        for result in results:
            if 'restingHeartrate' in result:
                data.append({
                    'date': result['date'],
                    'restingHeartRate': result['restingHeartrate'] # Resting heart rate value for the day (daily)
                })

        # Create a pandas dataframe from the list of dictionaries
        df = pd.DataFrame(data)

        # Save the dataframe to a CSV file with a descriptive file name
        # filename = f"heart_resting_heart_rate_{start_date_string}_{end_date_string}.csv"
        # df.to_csv(filename, index=False)

        # Return the pandas dataframe
        return df
    def dataframe_hrv(self, start_date=None, end_date=None):
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
            "type": "hrv", # Select documents with "type" equal to "heart"
            "date": { # Select documents where "date" is between the start and end dates
                "$gte": start_date_string, # Greater than or equal to start date
                "$lte": end_date_string  # Less than or equal to end date
            }
        }
        results = self.collection.find(query)

        # Extract heart rate data from the MongoDB documents and store it as a list of dictionaries
        data = []
        for result in results:
                data.append({
                    'date': result['date'],
                    'daily_rmssd': result['dailyRmssd'], # The Root Mean Square of Successive Differences (RMSSD) between heart beats. It measures short-term variability in the user’s daily heart rate in milliseconds (ms).
                    'deep_rmssd': result['deepRmssd'] # The Root Mean Square of Successive Differences (RMSSD) between heart beats. It measures short-term variability in the user’s heart rate while in deep sleep, in milliseconds (ms).
                })

        # Create a pandas dataframe from the list of dictionaries
        df = pd.DataFrame(data)

        # Save the dataframe to a CSV file with a descriptive file name
        # filename = f"heart_hrv_{start_date_string}_{end_date_string}.csv"
        # df.to_csv(filename, index=False)

        # Return the pandas dataframe
        return df

    def dataframe_sleep(self, start_date=None, end_date=None):
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

        # Query the MongoDB collection for sleep data between the start and end dates
        query = {
            "type": "sleep", # Select documents with "type" equal to "sleep"
            "date": { # Select documents where "date" is between the start and end dates
                "$gte": start_date_string, # Greater than or equal to start date
                "$lte": end_date_string  # Less than or equal to end date
            }
        }
        results = self.collection.find(query)

        # Extract sleep data from the MongoDB documents and store it as a list of dictionaries
        data = []

        for result in results:
            print(result)
            for item in result['data']:
                measurement = {
                    'date': item['dateTime'],
                    'level': item['level'],
                    'seconds': item['seconds']
                }
                data.append(measurement)

        # Create a pandas dataframe from the list of dictionaries
        df = pd.DataFrame(data)

        # Save the dataframe to a CSV file with a descriptive file name
        # filename = f"sleep_data_{start_date_string}_{end_date_string}.csv"
        # df.to_csv(filename, index=False)

        # Return the pandas dataframe
        return df

    def dataframe_sleep_metrics(self, start_date=None, end_date=None):
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

        # Query the MongoDB collection for sleep data between the start and end dates
        query = {
            "type": "sleep", # Select documents with "type" equal to "sleep"
            "date": { # Select documents where "date" is between the start and end dates
                "$gte": start_date_string, # Greater than or equal to start date
                "$lte": end_date_string  # Less than or equal to end date
            }
        }
        results = self.collection.find(query)

        # Extract sleep data from the MongoDB documents and store it as a list of dictionaries
        data = []

        for item in results:
            measurement = {
                'date': item['date'],
                'duration': item['metrics']['duration'],
                'efficiency': item['metrics']['efficiency'],
                'startTime': item['metrics']['startTime'],
                'endTime': item['metrics']['endTime'],
                'minutesAsleep': item['metrics']['minutesAsleep'],
                'minutesAwake': item['metrics']['minutesAwake'],
                'minutesToFallAsleep': item['metrics']['minutesToFallAsleep'],
                'minutesAfterWakeup': item['metrics']['minutesAfterWakeup'],
                'timeInBed': item['metrics']['timeInBed'],
            }
            data.append(measurement)

        # Create a pandas dataframe from the list of dictionaries
        df = pd.DataFrame(data)

        # Save the dataframe to a CSV file with a descriptive file name
        # filename = f"sleep_metrics_data_{start_date_string}_{end_date_string}.csv"
        # df.to_csv(filename, index=False)

        # Return the pandas dataframe
        return df

    def dataframe_sleep_summary(self, start_date=None, end_date=None):
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

        # Query the MongoDB collection for sleep data between the start and end dates
        query = {
            "type": "sleep", # Select documents with "type" equal to "sleep"
            "date": { # Select documents where "date" is between the start and end dates
                "$gte": start_date_string, # Greater than or equal to start date
                "$lte": end_date_string  # Less than or equal to end date
            }
        }
        results = self.collection.find(query)

        # Extract sleep data from the MongoDB documents and store it as a list of dictionaries
        data = []

        rows = []
        for doc in results:
            date = doc['date']
            for stage in ['deep', 'light', 'rem', 'wake']:
                if stage in doc['summary']:
                    minutes = doc['summary'][stage]['minutes']
                    count = doc['summary'][stage]['count']
                    rows.append([date, stage, minutes, count])
        df = pd.DataFrame(rows, columns=['date', 'stage', 'totalMinutesAsleep', 'totalSleepRecords'])

        # Save the dataframe to a CSV file with a descriptive file name
        # filename = f"sleep_summary_data_{start_date_string}_{end_date_string}.csv"
        # df.to_csv(filename, index=False)

        # Return the pandas dataframe
        return df

# EXAMPLE CODE
client = MongoClientDataframes(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
)
startTime = date(year = 2023, month =3, day = 27)
endTime =  date(year = 2023, month = 4, day = 27)
#client.dataframe_heart_rate(start_date=startTime)
#client.dataframe_heart_summary(start_date=startTime)
#client.dataframe_heart_resting_heart_rate(start_date=startTime)
#client.dataframe_hrv(start_date=startTime)
#client.dataframe_sleep(start_date=startTime)
#client.dataframe_sleep_metrics(start_date=startTime)
#client.dataframe_sleep_summary(start_date=startTime)