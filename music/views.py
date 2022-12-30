"""
TO DO!!!
-   Konserter i dag henter kun artister som allerede har vært sjekket ut, må trolig oppdatere med
    en funksjon som gjør det mulig å hente alle artiser som er i alle spillelister

-   Det må ligges en kobling opp mot hvilken by de ønsker å se. Enten ved å fortsette samme view,
    eller å lage en egen som tar med seg artist til en ny view

-   Det må lages en ny modell som kan lagre kosert informasjon fra ticketmaster, denne bør inneholde:
    - Artist, by, link til arragement, dato og klokkeslett.
    - Krever først at kunden lager et navn på "oversikten", slik at den kan hentes frem senere, og kan lage flere
"""

from django.shortcuts import render
from django.contrib.auth.signals import user_logged_in
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from accounts.models import CustomUser
from .models import UserInformation, UserPlaylists, PlaylistInformation

from spotify import get_token, get_user_information, get_user_playlists, get_playlist_tracks

"""
Functions for filling database
"""
def create_spotify_user(spotify_user, user_information):
    new_spotify = UserInformation()
    new_spotify.spotifyuser = spotify_user
    new_spotify.follower = user_information["followers"] 
    new_spotify.picture = user_information["image_url"]
    new_spotify.save()

def create_playlist_info(spotify_user, token):
    playlist_data = get_user_playlists(spotify_user, token)

    for playlist in playlist_data:
        new_playlist = UserPlaylists()
        new_playlist.spotifyuser = spotify_user
        new_playlist.playlistName = playlist
        new_playlist.numbSongs = playlist_data[playlist]["songs"]
        new_playlist.description = playlist_data[playlist]["description"]
        new_playlist.tracksLink = playlist_data[playlist]["tracks"]
        new_playlist.uri = playlist_data[playlist]["uri"]
        new_playlist.save()

def create_playlist_tracklist(url, key):
    token = get_token()
    playlist_content = get_playlist_tracks(url, token)

    for song in playlist_content:
        new_info = PlaylistInformation()
        new_info.playlistName = key
        new_info.artistName = playlist_content[song]["artist"]
        new_info.artistUrl = playlist_content[song]["artist_url"]
        new_info.songName = playlist_content[song]["song"]
        new_info.songLength = playlist_content[song]["song_length"]
        new_info.albumName = playlist_content[song]["album_name"]
        new_info.albumUrl = playlist_content[song]["album_url"]
        new_info.save()
    
    return playlist_content
    

"""
Functions for returning data to views
"""
def check_data(sender, user, **kwargs):
    active_user = user.username
    user_information = ""

    if active_user != 'andre':
        active_object = CustomUser.objects.filter(username = active_user)
        
        spotify_user = ""
        for user in active_object:
            spotify_user = user.spotifyuser

        spotify_information_user = UserInformation.objects.filter(spotifyuser = spotify_user)      
        if not spotify_information_user:
            token = get_token()
            user_information = get_user_information(spotify_user, token)
            create_spotify_user(spotify_user, user_information)
            create_playlist_info(spotify_user, token)

def get_spotify_user(active_user):
    active_object = CustomUser.objects.filter(username = active_user)

    spotify_user = ""
    for user in active_object:
        spotify_user = user.spotifyuser

    spotify_information_user = UserInformation.objects.filter(spotifyuser = spotify_user)
    
    user_content = {}
    for user in spotify_information_user:
        user_content[spotify_user] = {
            "followers": user.follower,
            "picture": user.picture
        }

    return user_content

def get_playlists(active_user):
    active_object = CustomUser.objects.filter(username = active_user)

    spotify_user = ""
    for user in active_object:
        spotify_user = user.spotifyuser

    spotify_playlists = UserPlaylists.objects.filter(spotifyuser = spotify_user).all()

    playlists = {}
    for list in spotify_playlists:
        playlists[list] = {
            "songs": list.numbSongs,
            "desc": list.description
        }

    return playlists

def get_track_information(key):
    tracklist_info = PlaylistInformation.objects.filter(playlistName = key).all()

    if not tracklist_info:
        url = UserPlaylists.objects.filter(playlistName = key).values('tracksLink').get()
        url = url['tracksLink']

        tracklist_info = create_playlist_tracklist(url, key)

    else:
        temp_info = {}
        num_song = 1

        for song in tracklist_info:
            temp_info[f"Song: {num_song}"] = {
                'artist': song.artistName,
                'artist_url': song.artistUrl,
                'song': song.songName,
                'song_length': song.songLength,
                'album_name': song.albumName,
                'album_url': song.albumUrl                  
            }

            num_song += 1
        
        tracklist_info = temp_info    

    return tracklist_info



"""
Views
"""
def index(request):
    active_user = request.user
    user_logged_in.connect(check_data)

    content = get_spotify_user(active_user)
    playlists = get_playlists(active_user)

    return render(request, 'home.html', {'content': content, 'playlists': playlists})


@login_required
def playlist_view(request):

    active_user = request.user
    playlists = get_playlists(active_user)

    return render(request, 'playlist.html', {'playlists': playlists})

@login_required
def playlist_information_view(request, key):

    songs = get_track_information(key)
    page = request.GET.get('page', 1)

    song_tuple = tuple(songs.items())
    paginator = Paginator(song_tuple, 20)

    try:
        table_paginator = paginator.page(page)
    except PageNotAnInteger:
        table_paginator = paginator.page(1)
    except EmptyPage:
        table_paginator = paginator.page(paginator.num_pages)

    content = {
        'info': table_paginator,
        'playlists': key
    }

    return render(request, 'playlist_information.html', content)

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