# accounts/forms.py
from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from .models import CustomUser

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = (
            "username",
            "firstname",
            "lastname",
            "spotifyuser",
            "email"
        )
        labels = {
            "username": "Username",
            "firstname": "First name",
            "lastname": "Last name",
            "spotifyuser": "Spotify username"
        }

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = CustomUser
        fields = (
            "username", 
            "firstname",
            "lastname",
            "spotifyuser",
            "email"
        )
        labels = {
            "username": "Username",
            "firstname": "First name",
            "lastname": "Last name",
            "spotifyuser": "Spotify username"
        }