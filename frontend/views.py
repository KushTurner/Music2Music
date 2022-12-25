from django.shortcuts import render, redirect
from django.http import HttpResponse
from frontend.util import *

# Create your views here.

def home(request):

    # Checks if access tokens have been retrieved in the session else set them to None
    try:
        request.session['SpotifyToken']
        request.session['YouTubeToken']

    except:
        request.session['SpotifyToken'] = None
        request.session['YouTubeToken'] = None
    
    # If both access tokens have been taken...
    if request.session['SpotifyToken'] != None and request.session['YouTubeToken'] != None:
        
        # Do something
        return redirect('convert')
       
    else:
        return render(request, 'index.html', {})

def convert(request):
    spotifytoken = request.session['SpotifyToken']

    youtubetoken = request.session['YouTubeToken']

    spotify_playlists = get_playlists(spotifytoken)

    if spotify_playlists == "expired":
        request.session['SpotifyToken'] = None
        request.session['YouTubeToken'] = None
        return redirect('home')
    
    context = {
            "playlists": spotify_playlists
        }
    
    if request.method == "POST":
        
        spotify_playlistID = request.POST['playlistID']
        playlist_name = request.POST['playlist_name']
        youtube_playlistID = create_playlist(playlist_name, youtubetoken)
        songtitles = titles_of_songs(spotify_playlistID, spotifytoken)
        youtubesongs = search_songs(songtitles, youtubetoken)
        populate_playlist(youtubesongs, youtube_playlistID, youtubetoken)
        
        redirect("/")
    
    return render(request, 'authorized.html', context)

def reset(request):
    request.session['SpotifyToken'] = None
    request.session['YouTubeToken'] = None
    return redirect('home')