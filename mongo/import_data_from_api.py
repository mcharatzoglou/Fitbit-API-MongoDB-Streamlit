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
        # with open('sleep_data.json') as json_file:
        #     sleep_data = json.load(json_file)

        # user_id = hashlib.sha256(b"example_user").hexdigest()
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
        heart_data = self.fitbit_api_client.get_heart_rate_data_for_datarange(startTime,endTime,detail_level)
        # with open('sleep_data.json') as json_file:
        #     sleep_data = json.load(json_file)

        # user_id = hashlib.sha256(b"example_user").hexdigest()
        user_id = hashlib.sha256(self.fitbit_api_client.USER_ID.encode('utf-8')).hexdigest()
        print(heart_data)
        # Iterate through sleep data
        for item in heart_data['activities-heart']:
            document = {
                "id": user_id,
                "type": "heart",
                "date": item['dateTime'],
                "heartRateZones": item['value']['heartRateZones']
            }
            self.collection.insert_one(document)

        intraday_data = heart_data['activities-heart-intraday']['dataset']
        intraday_document = {
            "id": user_id,
            "type": "intraday_heart",
            "date": heart_data['activities-heart-intraday']['dataset'],
            "data": intraday_data
        }
        self.collection.insert_one(intraday_document)
        return



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
client.import_heart_data_for_daterange(startTime=startTime,endTime=endTime)