from django.shortcuts import render
from django.http import HttpResponse

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
    
    if request.session['SpotifyToken'] and request.session['YouTubeToken']:
        
        # Do something
        
        return render(request, 'authorized.html', {})

    else:
        return render(request, 'index.html', {})
