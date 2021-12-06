'''

    Playlist class.

'''

from .song import Song

class Playlist():

    def __init__(self):
        self.__name: str = ''
        self.__total_songs: int = 0
        self.__songs: list = []
        self.__image: str = ''
        self.__description: str = ''

    def __repr__(self):
        return_string = '-----------------------------' + '\n'
        return_string += '--Name: ' + self.get_name() + '\n'
        return_string += '--Total: ' + str(self.get_total_songs()) + '\n'
        return_string += '--Cover URL: ' + self.get_image() + '\n'
        return_string += '--Description: ' + self.get_description() + '\n'
        return_string += '--Songs: ' + '\n'
        for song in self.get_songs():
            return_string += song.repr()
        return_string += '-----------------------------' + '\n'
        return return_string

    def repr(self) -> str:
        return_string = '-----------------------------' + '\n'
        return_string += '--Name: ' + self.get_name() + '\n'
        return_string += '--Total: ' + str(self.get_total_songs()) + '\n'
        return_string += '--Cover URL: ' + self.get_image() + '\n'
        return_string += '--Description: ' + self.get_description() + '\n'
        return_string += '-----------------------------' + '\n'
        return return_string

    def get_url(self) -> str:
        try:
            page = self.get_name().replace(" ", "-")
        except:
            page = self.get_name()
        return "/playlists/" + page

    def set_name(self, new_name: str):
        self.__name = new_name

    def get_name(self) -> str:
        return self.__name

    def set_total_songs(self, number:int):
        self.__total_songs = number

    def get_total_songs(self) -> int:
        return self.__total_songs

    def increment_total_songs(self):
        self.__total_songs += 1

    def decrement_total_songs(self):
        if self.__total_songs != 0:
            self.__total_songs -= 1
    
    def get_songs(self) -> list:
        return self.__songs

    def add_song(self, song: Song) -> bool:
        if song not in self.__songs:
            self.__songs.append(song)
            return True
        else:
            return False

    def remove_song(self, song: Song) -> bool:
        if (song in self.__songs):
            self.__songs.remove(song)
            return True
        else:
            return False

    def set_image(self, image: str):
        self.__image = image

    def get_image(self) -> str:
        return self.__image

    def set_description(self, description: str):
        self.__description = description

    def get_description(self) -> str:
        return self.__description

