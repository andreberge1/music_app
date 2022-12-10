"""

"""

import requests

class Playlist:
    def __init__(self, token, playlist):
        # API related information
        self._token = token
        self._headers = {
            'Authorization': f'Bearer {self._token}'
        }
        self._BASE_URL = 'https://api.spotify.com/v1/'

        # Class related information
        self._playlist_information_dict = playlist



    def _get_playlist_tracks(self, playlist_url):
        r = requests.get(playlist_url, headers=self._headers)
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
