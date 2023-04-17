# This is a python file you need to have in the same directory as your code so you can import it
import gather_keys_oauth2 as Oauth2
import fitbit

CLIENT_ID = '23QRJ6'
CLIENT_SECRET = 'abb49f0cdfcfd2605f02fcae11dda3b4'
def setup_fitbit_api_connection(client_id = CLIENT_ID, client_secret = CLIENT_SECRET):
    server=Oauth2.OAuth2Server(CLIENT_ID, CLIENT_SECRET)
    server.browser_authorize()
    ACCESS_TOKEN=str(server.fitbit.client.session.token['access_token'])
    REFRESH_TOKEN=str(server.fitbit.client.session.token['refresh_token'])
    auth2_client=fitbit.Fitbit(client_id,client_secret,oauth2=True,access_token=ACCESS_TOKEN,refresh_token=REFRESH_TOKEN)
    return auth2_client




