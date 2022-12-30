from django.contrib import admin
from .models import UserInformation, UserPlaylists, PlaylistInformation

# Register your models here.
admin.site.register(UserInformation)
admin.site.register(UserPlaylists)
admin.site.register(PlaylistInformation)