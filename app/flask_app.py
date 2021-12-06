'''

    Flask app for Spotify web interface.

'''

import traceback
from .src.user import User
from .config import display
from flask import Flask, render_template, request, redirect
from termcolor import colored

app = Flask(__name__, static_folder='instance/static')

user = User()

@app.route('/', methods=['GET', 'POST'])
def home():
    
    global user

    if (user.get_auth_status()):
        data = {
            'username': user.get_username(),
            'name': user.get_name(),
            'pfp_url': user.get_image(),
            'playlists': user.get_playlists()
        }
        return render_template('index.html', title='Home - SWI', show=display, data=data)
    else:
        return render_template('login.html', title='Login - SWI', show=display)

@app.route('/login', methods=['GET', 'POST'])
def login():

    global user

    # redirects to home if user is already logged in
    if (user.get_auth_status()):
        return redirect('/')
    
    try:
        # get secrets
        user.load_secrets()

        # build query string to get auth token
        query_string = ''
        query_string += User.AUTH_URL
        query_string += '?'
        query_string += 'client_id='
        query_string += user.get_secrets().get_client_id()
        query_string += '&response_type=code'
        query_string += '&redirect_uri=http://localhost:8097/get_auth_token'
        query_string += '&scope=user-read-private user-read-email playlist-read-private'
        query_string += '&show_dialog=true'
    
    except Exception as e:
        traceback.print_exc()    

    return redirect(query_string)

@app.route('/get_auth_token', methods=['GET', 'POST'])
def get_auth_token():

    global user

    if (user.get_auth_status()):
        return redirect('/')

    # gets auth token from argument
    auth_token = request.args.get('code')

    # sets auth token
    user.get_secrets().set_auth_token(auth_token)

    return redirect('/logging_in')

@app.route('/logging_in', methods=['GET', 'POST', 'PUT'])
def logging_in():

    global user

    if (user.get_auth_status()):
        return redirect('/')

    # gets access and refresh token
    if (user.authenticate()):
        user.set_auth_status(True)
        return redirect('/')
    else:
        return redirect('/error/bad-authentication')

@app.route('/error/<error>', methods=['GET'])
def error(error):
    
    errors = {
        'bad-auth': 'ERROR: There was an issue during authentication with Spotify.',
        'bad-playlist-name': 'ERROR: Could not find playlist with that name.'
    }

    try:
        error_message = errors[error]
    except:
        error_message = 'ERROR: Unknown Error.'

    data = {
        'error': error_message
    }

    return render_template('errors.html', data=data)

@app.route('/playlists/<name>', methods=['GET'])
def playlists(name):

    this_playlist = ''
    for playlist in user.get_playlists():
        if playlist.get_name().replace(" ", "-") == name:
            this_playlist = playlist

    if (this_playlist == ''):
        return redirect('/error/bad-playlist-name')

    data = {
        'playlist': this_playlist
    }

    return render_template('playlist.html', data=data)

    



    


if __name__ == '__main__':
    print(colored('ERROR: Run the app using run.py', 'red'))