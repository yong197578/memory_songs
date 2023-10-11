from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import config
while True:
    user_input = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
    if len(user_input) == 10 and user_input[4] == "-" and user_input[7] == "-":
        if user_input[:4].isdigit() and user_input[5:7].isdigit() and user_input[8:10].isdigit():
            break
    else:
        print("Invalid Format! Please Try Again")
response = requests.get(f"https://www.billboard.com/charts/hot-100/{user_input}")
top100 = response.text
soup = BeautifulSoup(top100, "html.parser")

song_names_spans = soup.select("li ul li h3")
song_names = [song.getText().strip() for song in song_names_spans]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=config.spotify_client_id,
        client_secret=config.spotify_secret_key,
        show_dialog=True,
        cache_path="token.txt",
    )
)
user_id = sp.current_user()["id"]
print(user_id)

song_uris = []
year = user_input.split("-")[0]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user=user_id, name=f"{user_input} Billboard 100", public=False)
print(playlist)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)