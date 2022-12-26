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
        
        # Redirect to convert page
        return redirect('convert')
    else:
        # Stay on homepage
        return render(request, 'index.html', {})

def convert(request):

    # Save Spotify access token in a variable
    spotifytoken = request.session['SpotifyToken']

    # Save YouTube access token in a variable
    youtubetoken = request.session['YouTubeToken']

    # Request selected spotify playlist
    spotify_playlists = get_playlists(spotifytoken)

    # If getting the playlist causes an error, restart session
    if spotify_playlists == "expired":
        request.session['SpotifyToken'] = None
        request.session['YouTubeToken'] = None
        return redirect('home')
    
    # Context needed to be passed into front end to be displayed
    context = {
            "playlists": spotify_playlists
        }
    
    # Check if user has submitted the form
    if request.method == "POST":
        
        # Get the playlist ID from the selected playlist
        spotify_playlistID = request.POST['playlistID']

        # Get the playlist name the user wants for the YouTube playlist
        playlist_name = request.POST['playlist_name']

        # Create the YouTube playlist with the playlist name
        youtube_playlistID = create_playlist(playlist_name, youtubetoken)

        request.session["youtube_playlistID"] = youtube_playlistID

        # Creates a list of song titles to be used to search for with YouTube's API
        songtitles = titles_of_songs(spotify_playlistID, spotifytoken)

        # Creates a list of song ID's which have been found on YouTube
        youtubesongs = search_songs(songtitles, youtubetoken)

        # Iterates through the song ID's and adds them individually to the YouTube playlist 
        populate_playlist(youtubesongs, youtube_playlistID, youtubetoken)
        
        return redirect('created')
    
    return render(request, 'authorized.html', context)

def reset(request):
    request.session['SpotifyToken'] = None
    request.session['YouTubeToken'] = None
    return redirect('home')

def created(request):
    youtube_playlistID = request.session["youtube_playlistID"]

    context = {
        "playlistID": youtube_playlistID
    }

    return render(request, 'created.html', context)
