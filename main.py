import spotipy
import random
import numpy as np
from spotipy.oauth2 import SpotifyOAuth

scope = 'playlist-modify-public'
username = input("Enter your Spotify username: ")

token = SpotifyOAuth(scope=scope, username=username)
objPlaylist = spotipy.Spotify(auth_manager=token)

# finding what activity the user would like this playlist made for
print("SpotiPlay creates a customized playlist for you whether you are sleeping, relaxing, cooking, or even working out!")
activity = int(input("Enter a number 1-4 based on what activity you would like a playlist for: "))


# creating an empty playlist + playlist object
playlistName = input("Enter a name for your playlist: ")
playlistBio = input("Enter a description for your playlist: ")
objPlaylist.user_playlist_create(user=username, name=playlistName, public=True, description=playlistBio)


# find the user's top artists
artistInput = input("Enter a artist: ")
topArtists = []

while artistInput != 'quit':
   create = objPlaylist.search(q=artistInput)
   topArtists.append(create['tracks']['items'][0]['album']['artists'][0]['uri'])
   artistInput = input("Enter another artist or type 'quit': ")


# collecting data on top songs of the user's top artists
topSongs = []
for j in topArtists:
   topSongsData = objPlaylist.artist_top_tracks(j)
   songData = topSongsData['tracks']
   for k in songData:
       topSongs.append(k['uri'])


# randomizing playlist
random.shuffle(topSongs)

# filtering top songs based on activity
curatedPlaylist = []

# energy = measure of intensity and activity
# valence = measure of musical positiveness conveyed by a track
while len(curatedPlaylist) <= 20:
   for s in topSongs[0:20]:
       trackData = objPlaylist.audio_features(s)
       for currSong in trackData[0:5]:
           if activity == 1:
               if 0 < currSong['energy'] < 0.4 and 0 < currSong['valence'] < 0.5:
                   curatedPlaylist.append(currSong['uri'])
           if activity == 2:
               if 0.2 < currSong['energy'] < 0.6 and 0.3 < currSong['valence'] < 0.7:
                   curatedPlaylist.append(currSong['uri'])
           if activity == 3:
               if 0.4 < currSong['energy'] < 0.8 and 0.5 < currSong['valence'] < 0.9:
                   curatedPlaylist.append(currSong['uri'])
                   # print("value ", currSong['uri'])
           if activity == 4:
               if 0.6 < currSong['energy'] < 1.0 and 0.6 < currSong['valence'] < 1.0:
                   curatedPlaylist.append(currSong['uri'])
           else:
               continue

start = objPlaylist.user_playlists(user=username)
play = start['items'][0]['id']

objPlaylist.user_playlist_add_tracks(user=username, playlist_id=play, tracks=curatedPlaylist)

print("Check your Spotify playlist now :)")