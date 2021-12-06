'''

    Unit testing for user, secrets, and playlist class.

'''

from src.user import User
import unittest

'''

    Creates a dummy class and tests methods.

'''
user = User()
client_id = ''
client_secret = ''

with open('creds.txt') as file:
    client_id = file.readline().rstrip()
    client_secret = file.readline().rstrip()

user.set_name('shawn')
user.set_username('shawnrodgers77')
user.set_image('https://i.scdn.co/image/ab6775700000ee85a9e98c4092d432c212f9c453')
user.get_secrets().set_auth_token('test-token')
user.get_secrets().set_access_token('test-token')
user.get_secrets().set_refresh_token('test-token')
user.get_secrets().initialize()



class TestSpotify(unittest.TestCase):

    
    def test_profile_data(self):
        global user
        print(user.get_username())
        self.assertTrue(user.get_username() == 'shawnrodgers77')
        self.assertTrue(user.get_name() == 'shawn')
    
    def test_secrets(self):
        global user, client_id, client_secret
        self.assertTrue(user.get_secrets().get_auth_token() == 'test-token')
        self.assertFalse(user.get_secrets().get_access_token == 'test-token')
        self.assertFalse(user.get_secrets().get_refresh_token == 'test-token')
        self.assertEqual(user.get_secrets().get_client_id(), client_id)
        self.assertEqual(user.get_secrets().get_client_secret(), client_secret)

    def test_playlists_retrived(self):
        global user
        self.assertTrue(len(user.get_playlists()) == 0)

    def test_pfp(self):
        global user
        url = 'https://i.scdn.co/image/ab6775700000ee85a9e98c4092d432c212f9c453'
        self.assertTrue(user.get_image() == url)

    def test_authentication(self):
        global user
        self.assertTrue(not user.get_auth_status())

if __name__ == '__main__':
    unittest.main()





    