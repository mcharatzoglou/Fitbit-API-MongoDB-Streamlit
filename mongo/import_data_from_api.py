from api.fitbit_client import FitbitApiClient
from datetime import date, timedelta
import hashlib
import pymongo
from pymongo.server_api import ServerApi



class FitbitMongoClient:
    """
    A class to import sleep and heart rate data from Fitbit API into a MongoDB database.
    """

    def __init__(self, connection_string, database, collection, fitbit_client_id, fitbit_client_secret):
        """
        Initialize the FitbitMongoClient with the given parameters.

        Args:
        - connection_string: MongoDB connection string
        - database: MongoDB database name
        - collection: MongoDB collection name
        - fitbit_client_id: Fitbit API client ID
        - fitbit_client_secret: Fitbit API client secret
        """
        try:
            # Connect to MongoDB
            self.mongo_client = pymongo.MongoClient(connection_string,server_api=ServerApi('1'))
            self.db = self.mongo_client[database]
            self.collection = self.db[collection]

            # Initialize Fitbit API client
            self.fitbit_api_client = FitbitApiClient(fitbit_client_id, fitbit_client_secret)

        except Exception as e:
            # If any error occurs, set objects to None and raise an exception
            self.mongo_client = None
            self.db = None
            self.collection = None
            self.fitbit_api_client = None
            raise Exception(e)

    def import_sleep_data_for_daterange(self, startTime=None, endTime=None):
        sleep_data = self.fitbit_api_client.get_sleep_data_for_data_range(startTime,endTime)
        user_id = hashlib.sha256(self.fitbit_api_client.USER_ID.encode('utf-8')).hexdigest()


        # Iterate through sleep data
        for item in sleep_data['sleep']:

            # Check if document already exists based on date
            existing_doc = self.collection.find_one({"id": user_id, "type": "sleep", "date": item['dateOfSleep']})
            if existing_doc:
                continue

            # Create document for each data record
            document = {
                "id": user_id,
                "type": "sleep",
                "date": item['dateOfSleep'],
                "metrics": {
                    "startTime": item['startTime'],
                    "endTime": item['endTime'],
                    "duration": item['duration'],
                    "efficiency": item['efficiency'],
                    "minutesAsleep": item['minutesAsleep'],
                    "minutesAwake": item['minutesAwake'],
                    "minutesAfterWakeup": item['minutesAfterWakeup'],
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
        """
        The function imports heart rate data from the Fitbit API for a given date range and saves it to a MongoDB collection.

        Args:
        startTime (str): Start date for data import in yyyy-MM-dd format. Defaults to None.
        endTime (str): End date for data import in yyyy-MM-dd format. Defaults to None.
        detail_level (str): Detail level for heart rate data. Must be one of "1sec", "1min", or "15min". Defaults to "1min".

        Returns:
        bool: Returns True if data was successfully imported and saved to the collection.
        """


        # Retrieve heart rate data from Fitbit API for specified date range and detail level
        multiple_heart_data = self.fitbit_api_client.get_heart_rate_data_for_data_range(startTime, endTime,
                                                                                        detail_level)

        # Hash user ID to maintain anonymity
        user_id = hashlib.sha256(self.fitbit_api_client.USER_ID.encode('utf-8')).hexdigest()

        # Iterate through each heart rate data point
        for heart_data in multiple_heart_data:
            # Check if the document already exists in the collection
            existing_document = self.collection.find_one(
                {"id": user_id, "type": "heart", "date": heart_data['activities-heart'][0]['dateTime']})
            if existing_document:
                continue  # Skip if document already exists
            # Extract relevant data and create a document to be inserted into the database
            document = {
                "id": user_id,
                "type": "heart",
                "date": heart_data['activities-heart'][0]['dateTime'],
                "heartRateZones": heart_data['activities-heart'][0]['value']['heartRateZones'],
                "heartIntraday": heart_data['activities-heart-intraday']['dataset']
            }

            # Check if resting heart rate data is present and add to document if available
            if 'restingHeartRate' in heart_data['activities-heart'][0]['value']:
                document['restingHeartrate'] = heart_data['activities-heart'][0]['value']['restingHeartRate']

            # Insert document into database collection
            self.collection.insert_one(document)

        # Return True to indicate successful data import
        return True

    def import_hrv_data_for_daterange(self, startTime=None, endTime=None):
        """
        The function imports Heart Rate Variability (HRV) from the Fitbit API for a given date range and saves it to a MongoDB collection.

        Args:
        startTime (str): Start date for data import in yyyy-MM-dd format. Defaults to None.
        endTime (str): End date for data import in yyyy-MM-dd format. Defaults to None.

        Returns:
        bool: Returns True if data was successfully imported and saved to the collection.
        """
        # Retrieve heart rate data from Fitbit API for specified date range and detail level
        multiple_hrv_data = self.fitbit_api_client.get_hrv_data_for_data_range(startTime, endTime)

        user_id = hashlib.sha256(self.fitbit_api_client.USER_ID.encode('utf-8')).hexdigest()

        for hrv in multiple_hrv_data['hrv']:

            existing_document = self.collection.find_one(
                {"id": user_id, "type": "hrv", "date": hrv['dateTime']})
            if existing_document:
                continue  # Skip if document already exists

            # Extract relevant data and create a document to be inserted into the database
            document = {
                "id": user_id,
                "type": "hrv",
                "date": hrv['dateTime'],
                "dailyRmssd": hrv['value']['dailyRmssd'],
                "deepRmssd": hrv['value']['deepRmssd']
            }

            # Insert document into database collection
            self.collection.insert_one(document)

        # Return True to indicate successful data import
        return True


# EXAMPLE CODE
client = FitbitMongoClient(
    connection_string="MONGO_URL_GOES_HERE",
    database="DATABASE_HERE",
    collection="COLLECTION_HERE",
    fitbit_client_id="FITBIT_CLIENT_ID_HERE",
    fitbit_client_secret="FITBIT_CLIENT_SECRET_HERE",
)
startTime = date(year = 2023, month = 4, day = 20)
endTime = date.today()
client.import_sleep_data_for_daterange()
client.import_heart_data_for_daterange()
client.import_hrv_data_for_daterange(startTime)