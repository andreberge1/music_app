"""

"""
import requests

class User:
    def __init__(self, token, username):
        # API related information:
        self._token = token             # token fra get_token()
        self._username = username       # spotify username
        self._headers = {
            'Authorization': f'Bearer {self._token}'
        }
        self._BASE_URL = 'https://api.spotify.com/v1/'

        # Class related information
        self._full_name = ""
        self._followers = 0
        self._image_url = ""
        self._playlist = self._get_user_playlists()


    def get_user_information(self):
        r = requests.get(self._BASE_URL+f"users/{self._username}",
            headers = self._headers)

        data = r.json()

        self._full_name = data["display_name"]
        self._followers = data["followers"]["total"],
        self._image_url = data["images"][0]["url"]


    def return_playlist(self):
        return self._playlist


    def return_user_info(self):
        user_info = {
            "username": self._username,
            "full_name": self._full_name,
            "followers": self._followers,
            "image_url": self._image_url
        }
        return user_info


    def _get_user_playlists(self):
        r = requests.get(self._BASE_URL+f"users/{self._username}/playlists/",
            headers = self._headers)

        data = r.json()
        playlists = {}

        for item in data["items"]:
            name = item["name"]
            desc = item["description"]
            tracks = item["tracks"]["href"]
            num_songs = item["tracks"]["total"]
            uri = item["uri"]

            playlists[name] = {
                "songs": num_songs,
                "description": desc,
                "tracks": tracks,
                "uri": uri,
            }

        return playlists

"""
def program():
    from spotify_token import get_token
    token = get_token()
    test = User(token, "andre008")
    test.get_user_information()
    lists = test.return_playlist()

    print("Test playslist")
    for item in lists:
        print(item, lists[item])

    print("test info")
    info = test.return_user_info()
    print(info)



program()
"""
