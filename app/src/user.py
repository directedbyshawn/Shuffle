'''

    User class.

'''

from .playlist import Playlist
from .song import Song
from .secrets import Secrets
import requests, base64, json

class User():

    AUTH_URL = 'https://accounts.spotify.com/authorize'
    TOKEN_URL = 'https://accounts.spotify.com/api/token'
    BASE_URL = 'https://api.spotify.com/v1/'

    def __init__(self):
        self.__username: str = ''
        self.__name: str = ''
        self.__secrets: Secrets = Secrets()
        self.__image: str = ''
        self.__authenticated = False
        self.__playlists: list = []

    def __repr__(self) -> str:
        return_string = '\n-----------------------------\n'
        return_string += 'Username: ' + self.get_username() + '\n'
        return_string += 'Display Name: ' + self.get_name() + '\n'
        return_string += 'PFP URL: ' + self.get_image() + '\n'
        return_string += 'Playlists: ' + '\n'
        for playlist in self.get_playlists():
            return_string += playlist.repr()
        return_string += '\n-----------------------------\n'
        return return_string
 
    def set_username(self, new_username: str):
        self.__username = new_username

    def get_username(self) -> str:
        return self.__username

    def set_name(self, new_name: str):
        self.__name = new_name

    def get_name(self) -> str:
        return self.__name

    def set_image(self, url: str):
        self.__image = url

    def get_image(self) -> str:
        return self.__image

    def set_auth_status(self, status: bool):
        self.__authenticated = status

    def get_auth_status(self) -> bool:
        return self.__authenticated

    def load_secrets(self) -> bool:
        return self.__secrets.initialize()
    
    def get_secrets(self) -> Secrets:
        return self.__secrets

    def get_headers(self) -> str:
        if (not self.__authenticated):
            return ''
        else:
            return {
                'Authorization': 'Bearer {token}'.format(token=self.__secrets.get_access_token())
            }

    def load_profile_info(self) -> bool:
        if (not self.__authenticated):
            return False
        else:
            
            # sets headers
            new_headers = self.get_headers()
            new_headers['Content-Type'] = 'application/json'
            new_headers['Accept'] = 'application/json'

            # sets endpoint
            endpoint = User.BASE_URL + 'me'

            # request
            profile_data = requests.get(endpoint,
                headers = new_headers
            )

            # convert response to json
            profile_data_json = profile_data.json()
            
            # sets profile info
            self.set_username(profile_data_json['id'])
            self.set_name(profile_data_json['display_name'])
            self.set_image(profile_data_json['images'][0]['url'])

            return True


    def load_playlists(self) -> bool:

        # ensures access token exists
        if (self.__secrets.get_access_token() == ''):
            return False

        # sets endpoint
        endpoint = User.BASE_URL + 'me/playlists'

        # sets headers
        new_headers = self.get_headers()
        new_headers['Content-Type'] = 'application/json'
        new_headers['Accept'] = 'application/json'

        # request
        playlist_data = requests.get(endpoint, 
            headers = new_headers
        )

        # data converted to json
        playlist_data_json = playlist_data.json()

        # adds each playlist to list
        playlist_list = playlist_data_json['items']
        for playlist in playlist_list:
            this_playlist = Playlist()

            # sets playlist data
            this_playlist.set_name(playlist['name'])
            this_playlist.set_total_songs(int(playlist['tracks']['total']))
            this_playlist.set_image(playlist['images'][0]['url'])
            this_playlist.set_description(playlist['description'])

            # tracks endpoint
            endpoint = playlist['tracks']['href']
            
            # tracks request
            song_data = requests.get(endpoint,
                headers=new_headers
            )

            song_data_json = song_data.json()
            track_list = song_data_json['items']

            for track in track_list:
                song = Song()

                # get data from response
                artist = track['track']['artists'][0]['name']
                title = track['track']['name']
                duration = track['track']['duration_ms']
                try:
                    cover = track['track']['album']['images'][0]['url']
                except:
                    cover = 'https://i.scdn.co/image/ab67616d0000b273b5e6aa732af786e368590e06'
                
                # set object attributes
                song.set_artist(artist)
                song.set_title(title)
                song.set_duration(duration)
                song.set_image(cover)

                this_playlist.add_song(song)

            # adds playlist to list of playlists
            self.__playlists.append(this_playlist)

        return True


    def get_playlists(self) -> list:
        return self.__playlists

    def add_playlist(self) -> bool:
        pass

    def add_to_playlist(self, playlist: Playlist,  song: Song) -> bool:
        pass

    def remove_from_playlist(self, playlist: Playlist, song: Song) -> bool:
        pass

    def authenticate(self) -> bool:

        '''
        
             Authenticates user with Spotify API. 

        '''

        # ensures user is not already authenticated

        if (self.__authenticated):
            return False
        else:

            # sets user status to authenticated
            self.set_auth_status(True)

            # client id & secret
            client_id = self.get_secrets().get_client_id()
            client_secret = self.get_secrets().get_client_secret()

            #conversion to b64 string
            message = '{id}:{secret}'.format(id=client_id, secret=client_secret)
            message_bytes = message.encode('ascii')
            base64_bytes = base64.b64encode(message_bytes)
            base64_message = base64_bytes.decode('ascii')

            # sets headers
            auth_param = 'Basic ' + base64_message
            headers = {
                'Authorization': auth_param,
                'Content-Type': 'application/x-www-form-urlencoded'
            }

            # sends request
            access_response = requests.post(User.TOKEN_URL, {
                'grant_type': 'authorization_code',
                'code': self.get_secrets().get_auth_token(),
                'redirect_uri': 'http://localhost:8097/get_auth_token'
            }, headers=headers)

            # parse requests
            access_response_data = access_response.json()

            # sets access token and refresh token
            self.get_secrets().set_access_token(access_response_data['access_token'])
            self.get_secrets().set_refresh_token(access_response_data['refresh_token'])

            # load user info and playlsits
            self.load_profile_info()
            self.load_playlists()  

            return True

            


