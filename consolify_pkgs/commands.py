from .global_functions import *
from .sp_module import sp


def nowplaying(args):
    current_song = sp.current_playback()
    if current_song is not None:
        song_name = current_song['item']['name']
        artists = ', '.join([artist['name'] for artist in current_song['item']['artists']])
        album = current_song['item']['album']['name']
        print(f""" 
Now playing: {song_name} by {artists}.""")
        if "-a" in args:
            print(f"Album: {album}")
        print(" ")
    else:
        print("""
No song currently playing.
        """)


def spotify_search(args):
    spotify_search_global(args)



def pause():
    current_playback = sp.current_playback()
    
    if current_playback is not None:
        # Check if Spotify is already paused
        if current_playback.get('is_playing', False):
            sp.pause_playback()
            print("Paused")
        else: 
            print("Spotify is already paused.")
    else:
        print("Can't pause, there is nothing playing.")


def play():
    current_playback = sp.current_playback()

    # Resume playback if there is a current playback
    if current_playback is not None:
        if current_playback.get('is_playing', False):
            print("Spotify is already playing.")
        else: 
            print("Resuming playback.")
            sp.start_playback()
    # Play recently played songs if there is no current playback
    else:
        recently_played = sp.current_user_recently_played(limit=10)

        # Check if there are recently played songs
        if recently_played and 'items' in recently_played:
            # Get the track URIs from the recently played songs
            track_uris = [item['track']['uri'] for item in recently_played['items']]

            # Choose a device for playback
            device_id = choose_device()

            # Check if the user chose to go back or no device was selected
            if device_id == "back":
                return "back"
            elif device_id is None:
                print("Playback aborted.")
                return

            # Start playback with the most recently played tracks on the chosen device
            sp.start_playback(uris=track_uris, device_id=device_id)
            print(f"Playing the most recently played track: {recently_played['items'][0]['track']['name']}")
        else:
            print("No recently played tracks found.")


def create_playlist(user_profile):
    playlist_name = input("Consolify/Playlist/Name > ")
    playlist = sp.user_playlist_create(user=user_profile['id'], name=playlist_name)
    print(f"\nCreated new playlist: {playlist_name}\n")
    print("Would you like to add songs now? (y, or any other input for no.)")
    add_songs_choice = input("Consolify/Playlist/Action > ")
    if add_songs_choice == "y":
        while True:
            result = add_songs_playlist(playlist['uri'])
            if result == "back":
                break
            print("Add another? (y, or any other input for no.)")
            choice = input("Consolify/Playlist/Action > ")
            if choice == "y":
                continue
            else:
                break
