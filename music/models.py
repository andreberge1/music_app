from django.db import models
from django.conf import settings


# Create your models here.
class UserInformation(models.Model):
    #username = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    spotifyuser = models.CharField(max_length=25)
    follower = models.IntegerField()
    picture = models.URLField()

    def __str__(self):
        return self.spotifyuser

    
class UserPlaylists(models.Model):
    spotifyuser = models.CharField(max_length=100)
    playlistName = models.CharField(max_length=100)
    numbSongs = models.IntegerField()
    description = models.CharField(max_length=500)
    tracksLink = models.CharField(max_length=100)
    uri = models.CharField(max_length=100)

    def __str__(self):
        return self.playlistName

class PlaylistInformation(models.Model):
    playlistName = models.CharField(max_length=100)
    artistName = models.CharField(max_length=100)
    artistUrl = models.CharField(max_length=100)
    songName = models.CharField(max_length = 100)
    songLength = models.CharField(max_length=10)
    albumName = models.CharField(max_length=100)
    albumUrl = models.CharField(max_length=100)

    def __str__(self):
        return self.playlistName



