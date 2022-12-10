"""
TODO:
get_playlist_tracks tar trenger en mulighet for å ligge flere sanger til
i ordboken, tar kun en nå
"""
import requests

# base URL of all Spotify API endpoints
BASE_URL = 'https://api.spotify.com/v1/'

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

def get_user_information(USER_ID, token, headers):
    r = requests.get(BASE_URL+f"users/{USER_ID}",
        headers = headers)

    data = r.json()

    user_info = {
        "full_name": data["display_name"],
        "followers": data["followers"]["total"],
        "image_url": data["images"][0]["url"]
    }

    return user_info


def get_user_playlists(USER_ID, token, headers):
    r = requests.get(BASE_URL+f"users/{USER_ID}/playlists/",
        headers = headers)

    data = r.json()

    playlists = {}

    for item in data["items"]:
        name = item["name"]
        desc = item["description"]
        tracks = item["tracks"]["href"]
        num_songs = item["tracks"]["total"]
        uri = item["uri"]

        details = get_playlist_tracks(tracks, token, headers)

        playlists[name] = {
            "songs": num_songs,
            "description": desc,
            "tracks": tracks,
            "uri": uri,
            "playlist_details": details
        }

    return playlists

def get_playlist_tracks(playlist_url, token, headers):
    r = requests.get(playlist_url, headers=headers)
    data = r.json()

    playlist_content = {}

    for item in data["items"]:
        artist = item["track"]["artists"][0]["name"]
        artist_url = item["track"]["artists"][0]["href"]
        song = item["track"]["name"]

        if artist in playlist_content.keys():
            playlist_content[artist]["songs"].append(song)
        else:
            playlist_content[artist] = {
                "songs": [song],
                "artist_url": artist_url
            }

    return playlist_content

def check_ticketmaster(artist):
    url = f"https://app.ticketmaster.com/discovery/v2/events?apikey=7elxdku9GGG5k8j0Xm8KWdANDgecHMV0&keyword={artist}&locale=no"

    r = requests.get(url)
    data = r.json()

    return data
