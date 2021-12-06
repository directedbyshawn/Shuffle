'''

    Song class.

'''

import math

class Song():

    def __init__(self):
        self.__artist: str = ''
        self.__title: str = ''
        self.__duration: list = []
        self.__image: str = ''

    def __repr__(self):
        return_string = '-----------------------------' + '\n'
        return_string += '----Artist: ' + self.get_artist() + '\n'
        return_string += '----Title: ' + str(self.get_title()) + '\n'
        return_string += '----Cover URL: ' + self.get_image() + '\n'
        return_string += '----Duration: ' + str(self.get_duration()[0]) + ' mins, ' + str(self.get_duration()[1]) + ' secs' + '\n'
        return_string += '-----------------------------' + '\n'
        return return_string
    
    def repr(self):
        return_string = '-----------------------------' + '\n'
        return_string += '----Artist: ' + self.get_artist() + '\n'
        return_string += '----Title: ' + str(self.get_title()) + '\n'
        return_string += '----Cover URL: ' + self.get_image() + '\n'
        return_string += '----Duration: ' + str(self.get_duration()[0]) + ' mins, ' + str(self.get_duration()[1]) + ' secs' + '\n'
        return_string += '-----------------------------' + '\n'
        return return_string

    def set_artist(self, new_artist: str):
        self.__artist = new_artist
    
    def get_artist(self) -> str:
        return self.__artist

    def set_title(self, new_title: str):
        self.__title = new_title

    def get_title(self) -> str:
        return self.__title

    def set_duration(self, duration_ms):

        if (type(duration_ms) != 'int'):
            ms = int(duration_ms)
        else:
            ms = duration_ms

        total_seconds = ms / 1000
        minutes = math.floor(total_seconds / 60)
        seconds = int(total_seconds % 60)

        self.__duration = [minutes, seconds]

    def get_duration(self) -> float:
        return self.__duration

    def set_image(self, new_image: str):
        self.__image = new_image
        
    def get_image(self) -> str:
        return self.__image
