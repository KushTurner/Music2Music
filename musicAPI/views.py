from django.shortcuts import render, HttpResponse, redirect
from django.http import HttpRequest

# Import secret keys
from dotenv import load_dotenv
import os

# Import APIview

import requests

load_dotenv()



# Create your views here.

def home(request):
    return HttpResponse("<h1>Authenticated</h1>")

# Authentication Page

def authSpotify(request):

    scopes = 'user-read-email'


    request = requests.get('https://accounts.spotify.com/authorize', params={
        'client_id': os.getenv('CLIENT_ID'),
        'response_type': 'code',
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'scope': scopes
    }).url
    
    return redirect(request)

# Redirect page

def callback(request):
    code = request.GET.get('code')
    error = request.GET.get('error')
    
    response = requests.post('https://accounts.spotify.com/api/token', data={
        'grant_type': 'authorization_code',
        'code': code,
        'redirect_uri': os.getenv('REDIRECT_URI'),
        'client_id': os.getenv('CLIENT_ID'),
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

    return redirect('mainapp:')
