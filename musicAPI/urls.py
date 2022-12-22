from django.urls import path
from . import views

app_name = 'authorization'

urlpatterns = [
    path('spotify-auth/', views.authSpotify),
    path('spotify-redirect/', views.redirectSpotify),
    path('youtube-auth/', views.authYoutube),
    path('youtube-redirect/', views.redirectYoutube),
]