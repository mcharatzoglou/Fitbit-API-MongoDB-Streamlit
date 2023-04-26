import pandas as pd
import fitbit
import api.gather_keys_oauth2 as Oauth2
from datetime import timedelta,datetime
import requests

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
            token = server.fitbit.client.session.token
            self.ACCESS_TOKEN = str(token['access_token'])
            self.REFRESH_TOKEN = str(token['refresh_token'])
            self.USER_ID = str(token['user_id'])
            self.fitbit_client = fitbit.Fitbit(
                client_id, client_secret, oauth2=True, access_token=self.ACCESS_TOKEN, refresh_token=self.REFRESH_TOKEN)
        except Exception as e:
            self.fitbit_client = None
            raise Exception(e)

    def get_sleep_data_for_data_range(self, startDate=None, endDate=None):
        """
        Retrieves sleep data for a specified date range. If no start or end date is provided, retrieves all sleep data.

        Args:
            start_date (str, optional): Start date of range in YYYY-MM-DD format. Defaults to None.
            end_date (str, optional): End date of range in YYYY-MM-DD format. Defaults to None.

        Returns:
            list: List of sleep data dictionaries. Each dictionary contains 'date' and 'duration' keys.
        """
        try:
            # Retrieve the user's join date
            user_profile = self.fitbit_client.user_profile_get()
            oldest_date = user_profile["user"]["memberSince"]
            oldest_date = datetime.strptime(oldest_date, "%Y-%m-%d").date()

            # Set the start date as the oldest available sleep data if start date is not specified
            startDate = startDate or oldest_date

            # Set the end date as yesterday's date if end date is not specified
            endDate = endDate or datetime.now().date() - timedelta(days=1)

            # Fitbit API endpoint
            url = f"https://api.fitbit.com/1.2/user/{self.USER_ID}/sleep/date/{startDate}/{endDate}.json"

            # Authorization header
            access_token = self.ACCESS_TOKEN
            headers = {"Authorization": f"Bearer {access_token}"}

            # Make the API request
            response = requests.get(url, headers=headers)

            # Check the response status code
            if response.status_code == 200:
                # Parse the sleep data from the JSON response
                sleep_data = response.json()
                return sleep_data
            else:
                print(f"Error retrieving sleep data: {response.status_code} - {response.text}")
                return None

        except Exception as e:
            print(f"Error retrieving sleep data: {e}")
            return None

    def get_heart_rate_data_for_data_range(self, startDate=None, endDate=None, detail_level="1min"):
        """
        Retrieve heart rate data for a specified date range, using the Fitbit API.

        Args:
            startDate (date, optional): The start date of the date range. If not specified, the oldest available heart rate data is used.
            endDate (date, optional): The end date of the date range. If not specified, yesterday's date is used.
            detail_level (str, optional): The level of detail for the data. Possible values are "1sec", "1min", and "15min". Default is "1min".

        Returns:
            heart_data (list): A list of dictionaries containing the heart rate data for each day in the specified date range.

        """

        # Retrieve the user's join date
        user_profile = self.fitbit_client.user_profile_get()
        oldest_date = user_profile["user"]["memberSince"]
        oldest_date = datetime.strptime(oldest_date, "%Y-%m-%d").date()

        # Set the start date as the oldest available HRV data if start date is not specified
        startDate = startDate or oldest_date

        # Set the end date as yesterday's date if end date is not specified
        endDate = endDate or datetime.now().date() - timedelta(days=1)

        # Generate a list of all dates in the specified range
        allDates = pd.date_range(start=startDate, end=endDate)

        # Fitbit API endpoint
        url = "https://api.fitbit.com/1/user/{user_id}/activities/heart/date/{oneDay}/1d/{detail_level}.json"

        # User and date information
        user_id = self.USER_ID

        # Authorization header
        access_token = self.ACCESS_TOKEN
        headers = {"Authorization": "Bearer " + access_token}

        # Make the API requests for each day in the range
        heart_data = []
        for d in allDates:
            # Construct the URL for the current date
            one_day_url = url.format(user_id=user_id, oneDay=d.strftime("%Y-%m-%d"), detail_level=detail_level)

            # Make the API request for the current date
            response = requests.get(one_day_url, headers=headers)

            # Check the response status code
            if response.status_code == 200:
                # Parse the heart rate data from the JSON response
                heart_data.append(response.json())
            else:
                # If the request fails, print an error message with the status code and response text
                print(f"Error retrieving heart rate data for {d}: {response.status_code} - {response.text}")

        return heart_data


    def get_hrv_data_for_data_range(self, startDate=None, endDate=None):
        """
        Retrieve Heart Rate Variability (HRV) data for a specified date range, using the Fitbit API.

        Args:
            startDate (date, optional): The start date of the date range. If not specified, the oldest available HRV data is used.
            endDate (date, optional): The end date of the date range. If not specified, yesterday's date is used.

        Returns:
            hrv_data (list): A list of dictionaries containing the HRV data for each day in the specified date range.

        """

        # Retrieve the user's join date
        user_profile = self.fitbit_client.user_profile_get()
        oldest_date = user_profile["user"]["memberSince"]
        oldest_date = datetime.strptime(oldest_date, "%Y-%m-%d").date()

        # Set the start date as the oldest available HRV data if start date is not specified
        startDate = startDate or oldest_date

        # Set the end date as yesterday's date if end date is not specified
        endDate = endDate or datetime.now().date() - timedelta(days=1)


        # Fitbit API endpoint
        url = f"https://api.fitbit.com/1/user/{self.USER_ID}/hrv/date/{startDate}/{endDate}.json"


        # Authorization header
        access_token = self.ACCESS_TOKEN
        headers = {"Authorization": f"Bearer {access_token}"}

        # Make the API request
        response = requests.get(url, headers=headers)

        # Check the response status code
        if response.status_code == 200:
            # Parse the sleep data from the JSON response
            hrv_data = response.json()
            return hrv_data
        else:
            print(f"Error retrieving sleep data: {response.status_code} - {response.text}")
            return None

