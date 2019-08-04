import json
import requests
import httplib2

from flask import (
    Flask,
    jsonify,
    session as login_session,
    redirect,
    url_for,
    request,
    make_response,
    render_template
)

import google_authentication as gAuth



# Set up the application
app = Flask(__name__)
try:
    app.secret_key = open('secret_key.txt', 'r').read()
except:
    print('Error: Please create a \'secret_key.txt\' file within the app\'s directory')


# Create data used to print into the user posts table
user_posts = [
    {"name": "Billy", "secret": "Likes Polka dot patterns, but will never admit it."},
    {"name": "Bobby", "secret": "Thinks Billy needs a shower."},
    {"name": "Lauren", "secret": "Wants John to ask her out"},
    {"name": "John", "secret": "Wants to ask Lauren out, but she's always so cold to him. He's not sure if he should ask her or not."}
]


@app.route('/')
def Index():
    return render_template(
        'index.html',
        client_id=gAuth.CLIENT_ID,
        authenticated=gAuth.Is_Authenticated(),
        user_posts=user_posts
    )

@app.route(gAuth.CLIENT_REDIRECT, methods=['POST'])
def Google_Authenticat():
    return gAuth.Authentication_Callback()

if __name__ == '__main__':
    app.debug = True
    app.run(
        host='0.0.0.0',
        port=5000
    )
