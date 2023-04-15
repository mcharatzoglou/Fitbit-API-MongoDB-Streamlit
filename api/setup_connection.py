# This is a python file you need to have in the same directory as your code so you can import it
import gather_keys_oauth2 as Oauth2
import fitbit
import pandas as pd
from datetime import date
CLIENT_ID='23QRJ6'
CLIENT_SECRET='abb49f0cdfcfd2605f02fcae11dda3b4'


server=Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
server.browser_authorize()
ACCESS_TOKEN=str(server.fitbit.client.session.token['access_token'])
REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
auth2_client=fitbit.Fitbit(CLIENT_ID,CLIENT_SECRET,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)



oneDate = date(year = 2023, month = 4, day = 14)
oneDayData = auth2_client.intraday_time_series('activities/heart', oneDate, detail_level='1sec')
df = pd.DataFrame(oneDayData['activities-heart-intraday']['dataset'])

# Look at the first 5 rows of the pandas DataFrame
df.head()

# The first part gets a date in a string format of YYYY-MM-DD
filename = oneDayData['activities-heart'][0]['dateTime'] +'_intradata'

# Export file to csv
df.to_csv(filename + '.csv', index = False)
df.to_excel(filename + '.xlsx', index = False)

