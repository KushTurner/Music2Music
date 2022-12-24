import requests
from urllib.parse import urlencode

# Creates YouTube playlist

def create_playlist(title, bearer, privacyStatus="public"):

    # Makes playlist public or private

    if privacyStatus != "public":
        privacyStatus = "private"
    
    # Endpoint needed to create playlist

    url = "https://www.googleapis.com/youtube/v3/playlists"

    # YouTube access token

    bearer = 'Bearer ' + bearer

    # Query parameters

    params = {
        "part": {
            "snippet", "status"
        }
    }

    # Payload 

    payload = {
        "snippet": {
            "title": title
        },

        "status": {
            "privacyStatus": privacyStatus
        }
    }

    # Headers 

    headers = {
        'Authorization': bearer,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Send post request to create playlist

    response = requests.post(url, params=params, json=payload, headers=headers)

    # Get playlist ID

    playlistId = response.json()["id"]

    # Pass playlist ID into session to access later.

    try: 
        session["YOUTUBE_PLAYLIST_ID"] = playlistId
    except:
        print("No session")
    
    return


# Returns names of playlists

def get_playlists(bearer):

    # Spotify access token

    bearer = "Bearer " + bearer

    # Endpoint needed to find playlists

    url = "https://api.spotify.com/v1/me/playlists"

    # Headers

    headers = {
        'Authorization': bearer,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Send GET request to retrieve playlist names

    response = requests.get(url, headers=headers)

    if response.status_code == 200:

        # Create playlist list to append a tuple with (songname, songid)

        playlists = []

        # Iterate through response to retrieve songname and songid

        for playlist in response.json().get("items"):

            # Get playlist id

            id = playlist["id"]

            # Get song name

            name = playlist["name"]

            # Append tuple with playlist name and id

            playlists.append((name, id))
    
    else:

        print(response.status_code)
    
    return playlists


# Return list of all songnames + artist from Spotify playlist


def selected_playlist(playlist_id, bearer):

    # Spotify access token

    bearer = "Bearer " + bearer

    # Endpoint needed to access selected playlist

    url = f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks?fields=items(track(name%2Cartists(name)))"

    # Headers

    headers = {
        'Authorization': bearer,
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    # Send GET request to retrieve songs from playlist
    
    response = requests.get(url, headers=headers)

    # List to be used to search using YouTube API eg. ("Song Name" "Artists")

    songs = []
    
    # Append values to list in specified format above

    for song in response.json()['items']:

        # Get artist names

        artist_list = song['track']['artists'][0].values()

        # Combine artists if there are multiple artists in a song to make YouTube search more specific

        artists = " ".join(artist for artist in artist_list)

        # Get track name
        
        trackname = song['track']['name']

        # Append song to songs list

        songs.append(trackname + " " + artists)
    
    return songs

# Iterate through list of songs and finds on YouTube

def search_songs(spotifylist: list, bearer):

    bearer = "Bearer " + bearer

    url = "https://www.googleapis.com/youtube/v3/search"

    headers = {
        'Authorization': bearer,
        'Accept': 'application/json',
    }

    amount_of_songs = 0

    song_ids = []
    

    for song in spotifylist:

        params = {
            "part": "snippet",
            "q": song,
            "maxResults": 1,
            "fields": "items(id(videoId),snippet(title))"
        }

        response = requests.get(url, params=params, headers=headers)
        videoId = response.json()["items"][0]["id"]["videoId"]
        song_ids.append(videoId)

    return song_ids

       
# Helper function

def add_song(videoId, playlistId, bearer):
    bearer = "Bearer " + bearer

    url = "https://www.googleapis.com/youtube/v3/playlistItems"

    headers = {
        'Authorization': bearer,
        'Accept': 'application/json',
    }

    params = {
        "part": {
            "snippet", "status"
        }
    }

    payload = {
        "snippet": {
            "playlistId": playlistId,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": videoId
            }
        }
    }

    response = requests.post(url, params=params, json=payload, headers=headers)
    
    return response.status_code

# Adds song to playlist

def populate_playlist(song_list: list, playlistId, bearer):
    for song in song_list:
        add_song(song, playlistId, bearer)


    

if __name__ == "__main__":
    # Testing
    testlist = ['Hey Now YoungBoy Never Broke Again', '50s Headie One', 'Alone Burna Boy', 'Just Wanna Rock Lil Uzi Vert', 'All In YoungBoy Never Broke Again', "Still Trappin' Lil Durk", 'Dis & That YoungBoy Never Broke Again', 'Middle of the Ocean Drake', 'Pussy & Millions (feat. Travis Scott) Drake', 'Treacherous Twins Drake']
    testlist2 = ['F5qe28eelAU', '13VbPLUhcgU', 'S8qGmBtXZV8', 'UhbixyxgsiU', '6MCSr65d9Xc', 'cDde7QlKCX0', 'QepL7wh-E80', 'IEueorPNpT0', '8LpAtRIakkk', 'jCtsnNpCDo0']
    # find_songs(testlist, "ya29.a0AX9GBdVJkp7rAFWY8buKDzx--WiBR8M_nxJB3anBy5mT7_35CAuFOl9UgDWTXiJc_ymkkf9RBwLIl88TrGn4DKHi4HDTTLO95X1SlU36MS0N2usD_UK83-bXnTyXucAYPVCLDGtY6dBIBou5yAhXAbFCHmN0aCgYKAR8SARISFQHUCsbCaGmb8IvN1JDVs9y4Mu9l2A0163")
    # populate_playlist(testlist2, "PLy4yrzjwxIfZboHPYlMC_D8VA9rCUfKiP", "ya29.a0AX9GBdWfJFEBNedgrkkuICploAUGieH87l2ANI6mrUA1sYw07qNGV1Xw6YfXTqjQPFhRWZ4mrjeY156s-5JNRawULzgyq45M-n2nIszuzH-Kplq9Ts0Gz5ZKofo91GkYDqjfKpoHrXpqP8CswVF0YIuff233aCgYKAesSARISFQHUCsbCvrGoXNd7FV9sxbUsR-YGQg0sxbUsR-YGQg0163")
    # populate_playlist(testlist, "PLy4yrzjwxIfZboHPYlMC_D8VA9rCUfKiP", "ya29.a0AX9GBdWfJFEBNedgrkkuICploAUGieH87l2ANI6mrUA1sYw07qNGV1Xw6YfXTqjQPFhRWZ4mrjeY156s-5JNRawULzgyq45M-n2nIszuzH-Kplq9Ts0Gz5ZKofo91GkYDqjfKpoHrXpqP8CswVF0YIuff233aCgYKAesSARISFQHUCsbCvrGoXNd7FV9sxbUsR-YGQg0sxbUsR-YGQg0163")
    
    # create_playlist("testing", "ya29.a0AX9GBdWfJFEBNedgrkkuICploAUGieH87l2ANI6mrUA1sYw07qNGV1Xw6YfXTqjQPFhRWZ4mrjeY156s-5JNRawULzgyq45M-n2nIszuzH-Kplq9Ts0Gz5ZKofo91GkYDqjfKpoHrXpqP8CswVF0YIuff233aCgYKAesSARISFQHUCsbCvrGoXNd7FV9sxbUsR-YGQg0sxbUsR-YGQg0163")

    # get_playlists("BQAlsaNJentVDPWNmBCFWtlbiLFPOQHc96GA1D2sQF9M5VKLryMFLPnTGdjuB5yvhGI28FjnLpQO_mcDChIwb1RTTCCTcUJdcXE32ixNzPkN6Kmy7HXQgxhCfMWTh0k0te3yR_mcE3KwvFC_zHdu4nnVPPa2LtIYM4KNezZgDOq-Ew_kaSZT-9VqFozh9mWVLW7n3cc8k_Txkqz5NMyjOVSLQMlJQKgPTN2pOwLW8vXtg-GsY9boMZ9hxaGrWHZm1atONA2PRZ1RTaM83qMG")