import json
import time
from api.fitbit_client import FitbitApiClient
from datetime import date,timedelta,datetime
import hashlib
import pymongo
from pymongo import MongoClient


class FitbitMongoClient():

    def __init__(self, connection_string, database, collection, fitbit_client_id, fitbit_client_secret):
        try:
            self.mongo_client = pymongo.MongoClient(connection_string)
            self.db = self.mongo_client[database]
            self.collection = self.db[collection]
            self.fitbit_api_client = FitbitApiClient(fitbit_client_id,fitbit_client_secret)
        except Exception as e:
            self.mongo_client = None
            #self.fitbit_api_client = None
            self.db = None
            self.collection = None
            raise Exception(e)


    def import_sleep_data_for_daterange(self, startTime=None, endTime=None):
        sleep_data = self.fitbit_api_client.get_sleep_data_for_datarange(startTime,endTime)
        user_id = hashlib.sha256(self.fitbit_api_client.USER_ID.encode('utf-8')).hexdigest()

        # Iterate through sleep data
        for item in sleep_data['sleep']:
            # Create document for each data record
            document = {
                "id": user_id,
                "type": "sleep",
                "dateOfSleep": item['dateOfSleep'],
                "metrics": {
                    "startTime": item['startTime'],
                    "endTime": item['endTime'],
                    "duration": item['duration'],
                    "efficiency": item['efficiency'],
                    "minutesAsleep": item['minutesAsleep'],
                    "minutesAwake": item['minutesAwake'],
                    "minutesToFallAsleep": item['minutesToFallAsleep'],
                    "timeInBed": item['timeInBed'],
                },
                "summary": item['levels']['summary'],
                "data": item['levels']['data'],

                }
            # Insert document into MongoDB
            self.collection.insert_one(document)
        return


    def import_heart_data_for_daterange(self, startTime=None, endTime=None, detail_level="1min"):
        multiple_heart_data = self.fitbit_api_client.get_heart_rate_data_for_datarange(startTime,endTime,detail_level)
        user_id = hashlib.sha256(self.fitbit_api_client.USER_ID.encode('utf-8')).hexdigest()
        # Iterate through sleep data
        for heart_data in multiple_heart_data:
            document = {
                "id": user_id,
                "type": "heart",
                "date": heart_data['activities-heart'][0]['dateTime'],
                "restingHeartrate": heart_data['activities-heart'][0]['value']['restingHeartRate'],
                "heartRateZones": heart_data['activities-heart'][0]['value']['heartRateZones'],
                "heartIntraday": heart_data['activities-heart-intraday']['dataset']
            }
            self.collection.insert_one(document)
        return True



client = FitbitMongoClient(
    connection_string = "mongodb://localhost:27017/",
    database="local",
    collection="fitbit",
    fitbit_client_id= "23QRJ6",
    fitbit_client_secret= "abb49f0cdfcfd2605f02fcae11dda3b4",
)
startTime = date(year = 2023, month = 4, day = 18)
endTime = date.today()
client.import_sleep_data_for_daterange()
client.import_heart_data_for_daterange()