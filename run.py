'''

    Launch flask app from here

'''

import traceback, os
from app.flask_app import app

def main():
    
    try:
        app.run(debug=app.debug, host='localhost', port=8097)
    except:
        traceback.print_exc()

if __name__ == '__main__':
    os.system('cls')
    main()
