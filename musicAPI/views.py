from django.shortcuts import render, redirect

# Import secret keys
from dotenv import load_dotenv
import os

# Import urlencode and requests
from urllib.parse import urlencode

import requests

# Load keys hidden in .env
load_dotenv()

# Create your views here.

# Authentication for Spotify
def authSpotify(request):

    # Get requirements needed from the users (view playlist)
    scopes = 'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public'

    # Send HTTP GET method to authorize user's acccount
    request = requests.get('https://accounts.spotify.com/authorize', params={
        'client_id': os.getenv('SPOTIFYCLIENT_ID'),
        'response_type': 'code',
        'redirect_uri': os.getenv('REDIRECT_URI_SPOTIFY'),
        'scope': scopes
    }).url

    # Redirects user to the page
    return redirect(request)

# Redirect page
def redirectSpotify(request):

    # Access the query parameters
    code = request.GET.get('code')
    error = request.GET.get('error')

    # Send HTTP POST method to redeem access token
    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI_SPOTIFY'),
        'client_id': os.getenv('SPOTIFYCLIENT_ID'),
        'client_secret': os.getenv('SPOTIFYSECRETKEY'),
    }).json()

    # Retrieve query paramters
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')

    # Add access token to session to be used when using API
    if access_token:
        request.session['SpotifyToken'] = access_token

    # Redirect back to homepage
    return redirect('/')


# Authentication for Amazon

def authYoutube(request):

    # Get requirements needed from the users (create playlist, add songs to playlists)
    scopes = ['https://www.googleapis.com/auth/youtube']

    # URL needed to authorize account
    auth_url = 'https://accounts.google.com/o/oauth2/auth'

    # Parameters to send with URL as a payload (eg ...?client_id=id)
    params={
        'client_id': os.getenv('YOUTUBECLIENT_ID'),
        'redirect_uri': os.getenv('REDIRECT_URI_YOUTUBE'),
        'response_type': 'code',
        'scope': ' '.join(scopes)
    }

    # Parameters need to be URL encoded for the web server be able to understand it
    auth_url += '?' + urlencode(params)

    # Redirect to the newly created authorization link
    return redirect(auth_url)



# Redirect page
def redirectYoutube(request):

    # Access the query parameters   
    code = request.GET.get('code')
    error = request.GET.get('error')

    # Send HTTP POST method to redeem access token
    response = requests.post('https://oauth2.googleapis.com/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI_YOUTUBE'),
        'client_id': os.getenv('YOUTUBECLIENT_ID'),
        'client_secret': os.getenv('YOUTUBESECRETKEY'),
    }).json()

    # Retrieve query paramters
    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    # Add access token to session database to be used when using API
    if access_token:
        request.session['YouTubeToken'] = access_token
    
    # Redirects user back to homepage
    return redirect('/')    