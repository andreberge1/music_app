from django.urls import path

from . import views

urlpatterns = [
    path('playlist/', views.playlist_view, name='playlist_view'),
    path('playlist/<str:key>', views.playlist_information_view, name='playlist_information'),
    path('concerts/', views.concert_overview, name=  'concert_overview'),
    path('concerts/<str:playlist>/', views.concert_overview, name=  'concert_overview'),
    path('concerts/<str:playlist>/<str:artist>', views.concert_overview, name=  'concert_overview')
]