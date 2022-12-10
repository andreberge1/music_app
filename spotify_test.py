import requests
from spotify import *


access_token = get_token()

headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}

# User ID
# USER_ID = 'renateek92'
USER_ID = 'andre008'

# playlist = "RA(w)R <3"

# User testing
#user_info = get_user_information(USER_ID, access_token, headers)
#print(user_info)



# Playlist testing
#playlists = get_user_playlists(USER_ID, access_token, headers)
#print(playlists)


# Plylist informasjon
# playlist_url = playlists[playlist]["tracks"]
# playlist_content = get_playlist_tracks(playlist_url, access_token, headers)

# for key in playlist_content.keys():
#    found = check_ticketmaster(key)
#    print(found)
