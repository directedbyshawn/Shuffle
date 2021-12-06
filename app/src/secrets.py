'''

    Class to retrieve tokens and other secrets.

'''

import os

class Secrets():

    FILE_PATH = "creds.txt"

    def __init__(self):
        self.__client_id: str = ""
        self.__client_secret: str = ""
        self.__auth_token: str = ""
        self.__access_token: str = ""
        self.__refresh_token: str = ""
    
    def initialize(self) -> bool:
        if (not os.path.exists(Secrets.FILE_PATH)):
            return False
        else:
            try:
                with open(Secrets.FILE_PATH) as file:
                    self.set_client_id(file.readline().rstrip())
                    self.set_client_secret(file.readline().rstrip())
                return True
            except:
                return False

    

    def set_client_id(self, client_id: str):
        self.__client_id = client_id

    def get_client_id(self) -> int:
        return self.__client_id

    def set_client_secret(self, client_secret: str):
        self.__client_secret = client_secret

    def get_client_secret(self) -> str:
        return self.__client_secret

    def set_auth_token(self, token: str):
        self.__auth_token = token

    def get_auth_token(self) -> str:
        return self.__auth_token

    def set_access_token(self, token: str):
        self.__access_token = token

    def get_access_token(self) -> str:
        return self.__access_token

    def set_refresh_token(self, token: str):
        self.__refresh_token = token

    def get_refresh_token(self) -> str:
        return self.__refresh_token

    