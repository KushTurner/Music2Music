from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpRequest

# Import secret keys
from dotenv import load_dotenv
import os

# Import urllib

from urllib.parse import urlencode

# Import APIview

import requests

load_dotenv()



# Create your views here.

# Authentication for Spotify

def authSpotify(request):

    scopes = 'playlist-read-private playlist-read-collaborative playlist-modify-private playlist-modify-public'


    request = requests.get('https://accounts.spotify.com/authorize', params={
        'client_id': os.getenv('SPOTIFYCLIENT_ID'),
        'response_type': 'code',
        'redirect_uri': os.getenv('REDIRECT_URI_SPOTIFY'),
        'scope': scopes
    }).url
    
    return redirect(request)

# Redirect page

def redirectSpotify(request):
    code = request.GET.get('code')
    error = request.GET.get('error')

    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI_SPOTIFY'),
        'client_id': os.getenv('SPOTIFYCLIENT_ID'),
        'client_secret': os.getenv('SPOTIFYSECRETKEY'),
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    refresh_token = response.get('refresh_token')
    expires_in = response.get('expires_in')

    print(access_token)
    print(token_type)
    print(refresh_token)
    print(expires_in)

    return redirect('/')


# Authentication for Amazon

def authYoutube(request):

    scopes = ['https://www.googleapis.com/auth/youtube']

    auth_url = 'https://accounts.google.com/o/oauth2/auth'

    params={
        'client_id': os.getenv('YOUTUBECLIENT_ID'),
        'redirect_uri': os.getenv('REDIRECT_URI_YOUTUBE'),
        'response_type': 'code',
        'scope': ' '.join(scopes)
    }

    auth_url += '?' + urlencode(params)

    
    return redirect(auth_url)


# Redirect page

def redirectYoutube(request):

    code = request.GET.get('code')
    error = request.GET.get('error')

    response = requests.post('https://oauth2.googleapis.com/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI_YOUTUBE'),
        'client_id': os.getenv('YOUTUBECLIENT_ID'),
        'client_secret': os.getenv('YOUTUBESECRETKEY'),
    }).json()

    access_token = response.get('access_token')
    token_type = response.get('token_type')
    expires_in = response.get('expires_in')

    print(access_token)
    print(token_type) 
    print(expires_in)

    return redirect('/')    