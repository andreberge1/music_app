import requests

def get_token():
    CLIENT_ID = "75044b2aaa2b47df97ecce1d6c78e81e"
    CLIENT_SECRET = "56a02a6e9e0f466ab44b77f87de05794"

    AUTH_URL = 'https://accounts.spotify.com/api/token'

    # POST
    auth_response = requests.post(AUTH_URL, {
        'grant_type': 'client_credentials',
        'client_id': CLIENT_ID,
        'client_secret': CLIENT_SECRET,
    })

    # convert the response to JSON
    auth_response_data = auth_response.json()

    # save the access token
    access_token = auth_response_data['access_token']

    return access_token
