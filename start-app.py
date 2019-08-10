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


def Is_Authenticated():
    return ('user' in login_session)

@app.route('/authenticated')
def Authenticated():
    if Is_Authenticated():
        return make_response(jsonify(message="User is already logged in", status=200, data=True))
    else:
        return make_response(jsonify(message="User is not logged in", status=200, data=False))


@app.route('/')
def Index():
    return render_template(
        'index.html',
        client_id=gAuth.CLIENT_ID,
        authenticated=Is_Authenticated(),
        user_posts=user_posts
    )


@app.route(gAuth.CLIENT_REDIRECT, methods=['POST'])
def Google_Authenticate():
    
    if not Is_Authenticated():
        response, user_data = gAuth.Authentication_Callback()
        login_session['user'] = user_data
        print(login_session['user'])

        return response
    
    if 'logout' in request.form:
        if Is_Authenticated():
            login_session.pop('user', None)

    return make_response(jsonify(message="Already logged in", status=200, data="Already Logged In"))

if __name__ == '__main__':
    app.debug = True
    app.run(
        ssl_context="adhoc",
        host='0.0.0.0',
        port=5000
    )
