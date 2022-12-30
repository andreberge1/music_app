@login_required
def concert_overview(request, playlist=None, artist=None):
    active_user = request.user
    active_object = CustomUser.objects.filter(username = active_user)

    spotify_user = ""
    for user in active_object:
        spotify_user = user.spotifyuser

    if playlist is not None:
        if artist is not None:
            content = {
                'playlists': playlist,
                'artists': artist
            }

            return render(request, 'concert_overview.html', content)

        else:
            query_user_artists = PlaylistInformation.objects.filter(playlistName = playlist).values('artistName').distinct()

            user_artists = []
            for query in query_user_artists:
                user_artists.append(query['artistName'])

            content = {
                'playlists': playlist,
                'artist_choice': user_artists
            }

    else:
        query_user_playlist = UserPlaylists.objects.filter(spotifyuser = spotify_user)
        query_user_artists = PlaylistInformation.objects.values('artistName').distinct()

        user_playlist = []
        user_artists = []

        for query in query_user_playlist:
            user_playlist.append(query.playlistName)

        for query in query_user_artists:
            user_artists.append(query['artistName'])

        content = {
            'playlist_choice': user_playlist,
            'artist_choice': user_artists
        }

    return render(request, 'concert_overview.html', content)