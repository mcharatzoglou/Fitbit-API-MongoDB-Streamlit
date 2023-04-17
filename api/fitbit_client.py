import pandas as pd
import fitbit
import api.gather_keys_oauth2 as Oauth2


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
            ACCESS_TOKEN = str(server.fitbit.client.session.token['access_token'])
            REFRESH_TOKEN = str(server.fitbit.client.session.token['refresh_token'])
            self.fibit_client = fitbit.Fitbit(client_id, client_secret, oauth2=True, access_token=ACCESS_TOKEN, refresh_token=REFRESH_TOKEN)
        except Exception as e:
            self.fibit_client = None
            raise Exception(e)


    def get_sleep_for_daterange(self, start_date=None, end_date=None):

        date_list = []
        df_list = []
        stages_df_list = []

        allDates = pd.date_range(start=startTime, end=endTime)

        for oneDate in allDates:
            oneDate = oneDate.date().strftime("%Y-%m-%d")

            oneDayData = self.fibit_client.sleep(date=oneDate)

            # get number of minutes for each stage of sleep and such.
            print(oneDayData['summary'])
            try:
                stages_df = pd.DataFrame(oneDayData['summary'])
            except: continue

            df = pd.DataFrame(oneDayData['sleep'][0]['minuteData'])

            date_list.append(oneDate)

            df_list.append(df)

            stages_df_list.append(stages_df)

        final_df_list = []

        final_stages_df_list = []

        for date, df, stages_df in zip(date_list, df_list, stages_df_list):

            if len(df) == 0:
                continue

            df.loc[:, 'date'] = pd.to_datetime(date)

            stages_df.loc[:, 'date'] = pd.to_datetime(date)

            final_df_list.append(df)
            final_stages_df_list.append(stages_df)

        final_df = pd.concat(final_df_list, axis=0)

        final_stages_df = pd.concat(final_stages_df_list, axis=0)

        columns = final_stages_df.columns[~final_stages_df.columns.isin(['date'])].values

        pd.concat([final_stages_df[columns] + 2, final_stages_df[['date']]], axis=1)

        # Export file to csv
        final_df.to_csv('minuteSleep' + '.csv', index=False)
        final_stages_df.to_csv('minutesStagesSleep' + '.csv', index=True)
