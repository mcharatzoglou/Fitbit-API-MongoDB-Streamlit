import pandas as pd
import fitbit
import api.gather_keys_oauth2 as Oauth2
from datetime import date,timedelta,datetime
import requests
import csv
import json

class FitbitApiClient:
    """
    A class that represents a Fitbit API client and provides methods for retrieving and exporting data.
    """

    def __init__(self, client_id, client_secret):
        """
        Initializes a FitbitApiClient instance.

        :param client_id: The client ID of the Fitbit API application.
        :param client_secret: The client secret of the Fitbit API application.
        """
        try:
            server = Oauth2.OAuth2Server(client_id, client_secret)
            server.browser_authorize()
            self.ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
            self.REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
            self.USER_ID = str(server.fitbit.client.session.token['user_id'])
            self.fitbit_client = fitbit.Fitbit(client_id, client_secret, oauth2=True, access_token=self.ACCESS_TOKEN, refresh_token=self.REFRESH_TOKEN)
        except Exception as e:
            self.fitbit_client = None
            raise Exception(e)

    def get_all_hrv_data(self, startDate=None, endDate=None):
        # Fitbit API endpoint
        url = "https://api.fitbit.com/1/user/{user_id}/hrv/date/{date}.json"
        #url = "https://api.fitbit.com/1.2/user/{user_id}/sleep/date/{date}.json"

        # User and date information
        user_id = self.USER_ID
        date = "2023-04-21"

        # Authorization header
        access_token = self.ACCESS_TOKEN
        headers = {"Authorization": "Bearer " + access_token}

        # Make the API request
        print(url.format(user_id=user_id, date=date))
        response = requests.get(url.format(user_id=user_id, date=date), headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Parse the HRV data from the JSON response
            hrv_data = response.json()
            print(hrv_data)
        else:
            print("Error:", response.status_code, response.text)

    def get_sleep_data_for_datarange(self,startDate=None,endDate=None):
        # Retrieve the user's join date
        user_profile = self.fitbit_client.user_profile_get()
        oldest_date = user_profile["user"]["memberSince"]
        oldest_date = datetime.strptime(oldest_date, "%Y-%m-%d").date()

        # Set the start date as the oldest available HRV data if start date is not specified
        startDate = startDate or oldest_date

        # Set the end date as yesterday's date if end date is not specified
        endDate = endDate or datetime.now().date() - timedelta(days=1)

        # Fitbit API endpoint
        url = "https://api.fitbit.com/1.2/user/{user_id}/sleep/date/{start_date}/{end_date}.json"

        # User and date information
        user_id = self.USER_ID

        # Authorization header
        access_token = self.ACCESS_TOKEN
        headers = {"Authorization": "Bearer " + access_token}

        # Make the API request
        response = requests.get(url.format(user_id=user_id, start_date=startDate, end_date=endDate), headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Parse the sleep data from the JSON response
            sleep_data = response.json()
            return sleep_data
        else:
            print("Error:", response.status_code, response.text)
            return None

    def get_heart_rate_data_for_datarange(self, startDate=None, endDate=None, detail_level="1min"):
        # Retrieve the user's join date
        user_profile = self.fitbit_client.user_profile_get()
        oldest_date = user_profile["user"]["memberSince"]
        oldest_date = datetime.strptime(oldest_date, "%Y-%m-%d").date()

        # Set the start date as the oldest available HRV data if start date is not specified
        startDate = startDate or oldest_date

        # Set the end date as yesterday's date if end date is not specified
        endDate = endDate or datetime.now().date() - timedelta(days=1)
        allDates = pd.date_range(start=startDate,end=endDate)
        # Fitbit API endpoint
        url = "https://api.fitbit.com/1/user/{user_id}/activities/heart/date/{oneDay}/1d/{detail_level}.json"

        # User and date information
        user_id = self.USER_ID

        # Authorization header
        access_token = self.ACCESS_TOKEN
        headers = {"Authorization": "Bearer " + access_token}

        # Make the API requests
        heart_data = []
        for d in allDates:
            # Construct the URL for the current date
            one_day_url = url.format(user_id=user_id, oneDay=d.strftime("%Y-%m-%d"), detail_level=detail_level)
            print(one_day_url)

            # Make the API request for the current date
            response = requests.get(one_day_url, headers=headers)

            # Check the response status code
            if response.status_code == 200:
                # Parse the heart rate data from the JSON response
                heart_data.append(response.json())
            else:
                print(f"Error retrieving heart rate data for {d}: {response.status_code} - {response.text}")

        # Save the heart rate data to a file
        with open("heart_rate.json", "w") as outfile:
            json.dump(heart_data, outfile)

        return heart_data


CLIENT_ID = '23QRJ6'
CLIENT_SECRET = 'abb49f0cdfcfd2605f02fcae11dda3b4'
# item = FitbitApiClient(CLIENT_ID,CLIENT_SECRET)
# hrv_data_by_date = item.get_all_hrv_data()
# hrv_data_by_date = item.get_all_hrv_data(startTime,endTime)
startTime = date(year = 2023, month = 4, day = 18)
endTime = date.today()

