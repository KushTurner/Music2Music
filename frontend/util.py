import requests

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
    
    return playlistId

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
        playlists = {}

        # Iterate through response to retrieve songname and songid
        for playlist in response.json().get("items"):

            # Get playlist id
            id = playlist["id"]

            # Get song name
            name = playlist["name"]

            # Append tuple with playlist name and id
            playlists[id] = name
    
    else:
        return "expired"
    
    return playlists


# Return list of all songnames + artist from Spotify playlist

def titles_of_songs(playlist_id, bearer):

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

    # YouTube access key
    bearer = "Bearer " + bearer

    # Endpoint needed to search for song on YouTube
    url = "https://www.googleapis.com/youtube/v3/search"

    # Headers
    headers = {
        'Authorization': bearer,
        'Accept': 'application/json',
    }

    # List of song ID'
    song_ids = []
    
    # Iterate through spotify playlist
    for song in spotifylist:

        # Query parameters
        params = {
            "part": "snippet",
            "q": song,
            "maxResults": 1,
            "fields": "items(id(videoId),snippet(title))"
        }

        # Send GET request to get list of songs
        response = requests.get(url, params=params, headers=headers)
        
        # Extract Video ID 
        videoId = response.json()["items"][0]["id"]["videoId"]
        
        # Append song ID to list
        song_ids.append(videoId)

    # Return list of song ID's
    return song_ids

# Add songs to playlist (helper function)
def add_song(videoId, playlistId, bearer):

    # YouTube access token
    bearer = "Bearer " + bearer

    # Endpoint to add YouTube song to playlist
    url = "https://www.googleapis.com/youtube/v3/playlistItems"

    # Headers
    headers = {
        'Authorization': bearer,
        'Accept': 'application/json',
    }

    # Query parameters
    params = {
        "part": {
            "snippet", "status"
        }
    }

    # Payload
    payload = {
        "snippet": {
            "playlistId": playlistId,
            "resourceId": {
                "kind": "youtube#video",
                "videoId": videoId
            }
        }
    }

    # Send POST request to add song to playlist
    response = requests.post(url, params=params, json=payload, headers=headers)
    
    # Returns status code (Successful = 200)
    return response.status_code

# Adds song to playlist
def populate_playlist(song_list: list, playlistId, bearer):

    # Iterate through list of song ID's
    for song in song_list:
        
        # Add song to playlist 
        add_song(song, playlistId, bearer)


    

if __name__ == "__main__":
    # Testing
    testlist = ['Hey Now YoungBoy Never Broke Again', '50s Headie One', 'Alone Burna Boy', 'Just Wanna Rock Lil Uzi Vert', 'All In YoungBoy Never Broke Again', "Still Trappin' Lil Durk", 'Dis & That YoungBoy Never Broke Again', 'Middle of the Ocean Drake', 'Pussy & Millions (feat. Travis Scott) Drake', 'Treacherous Twins Drake']
    testlist2 = ['F5qe28eelAU', '13VbPLUhcgU', 'S8qGmBtXZV8', 'UhbixyxgsiU', '6MCSr65d9Xc', 'cDde7QlKCX0', 'QepL7wh-E80', 'IEueorPNpT0', '8LpAtRIakkk', 'jCtsnNpCDo0']
    # find_songs(testlist, "ya29.a0AX9GBdVJkp7rAFWY8buKDzx--WiBR8M_nxJB3anBy5mT7_35CAuFOl9UgDWTXiJc_ymkkf9RBwLIl88TrGn4DKHi4HDTTLO95X1SlU36MS0N2usD_UK83-bXnTyXucAYPVCLDGtY6dBIBou5yAhXAbFCHmN0aCgYKAR8SARISFQHUCsbCaGmb8IvN1JDVs9y4Mu9l2A0163")
    # populate_playlist(testlist2, "PLy4yrzjwxIfZboHPYlMC_D8VA9rCUfKiP", "ya29.a0AX9GBdWfJFEBNedgrkkuICploAUGieH87l2ANI6mrUA1sYw07qNGV1Xw6YfXTqjQPFhRWZ4mrjeY156s-5JNRawULzgyq45M-n2nIszuzH-Kplq9Ts0Gz5ZKofo91GkYDqjfKpoHrXpqP8CswVF0YIuff233aCgYKAesSARISFQHUCsbCvrGoXNd7FV9sxbUsR-YGQg0sxbUsR-YGQg0163")
    # populate_playlist(testlist, "PLy4yrzjwxIfZboHPYlMC_D8VA9rCUfKiP", "ya29.a0AX9GBdWfJFEBNedgrkkuICploAUGieH87l2ANI6mrUA1sYw07qNGV1Xw6YfXTqjQPFhRWZ4mrjeY156s-5JNRawULzgyq45M-n2nIszuzH-Kplq9Ts0Gz5ZKofo91GkYDqjfKpoHrXpqP8CswVF0YIuff233aCgYKAesSARISFQHUCsbCvrGoXNd7FV9sxbUsR-YGQg0sxbUsR-YGQg0163")
    
    create_playlist("testing", "ya29.a0AX9GBdX3ElyysmJNKDOr2HQx_lHExneitogapo84qguoXmcv_7Ncw9_yK2sr99c1LykuEuYhSj427K3eu0kl-g07TEouNT2n6iGdWbTa2wcTE8MccdqUv2EvG57lpyzkwJRgsVeu1Ma-zfLx2pHaqfa7Y_OxaCgYKAdQSARISFQHUCsbCA7RpJyA_o6DWrXiOa8o6Mw0163")

    # get_playlists("BQAlsaNJentVDPWNmBCFWtlbiLFPOQHc96GA1D2sQF9M5VKLryMFLPnTGdjuB5yvhGI28FjnLpQO_mcDChIwb1RTTCCTcUJdcXE32ixNzPkN6Kmy7HXQgxhCfMWTh0k0te3yR_mcE3KwvFC_zHdu4nnVPPa2LtIYM4KNezZgDOq-Ew_kaSZT-9VqFozh9mWVLW7n3cc8k_Txkqz5NMyjOVSLQMlJQKgPTN2pOwLW8vXtg-GsY9boMZ9hxaGrWHZm1atONA2PRZ1RTaM83qMG")
    # print(search_songs(testlist, "ya29.a0AX9GBdW_iqx0HqkCTbaWMJ_wEm49KnfVl-zEHZF80ZkTCSv6d-37IknxsPy17DpYm4pyzDkPtk6o7TKlIa-tjwUorv-QBn-lEm4fd3Zt-MfjAEIln_HXj63vtq7lIqT_My1L_Vbx7zProtXGSpADYbYgqt3SaCgYKAVASARISFQHUCsbCRlvMclDinQpq1W5WBuHwEQ0163"))