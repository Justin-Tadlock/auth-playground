import json
import requests
import httplib2
import string
import random
import sys

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

from flask_cors import CORS, cross_origin

import google_authentication as gAuth
import facebook_authentication as fbAuth


# Set up the application
app = Flask(__name__)
try:
    app.secret_key = open('secret_key.txt', 'r').read()
except IOError as ioe:
    print('Error: Please create a \'secret_key.txt\' file within the app\'s directory')
    print(ioe.pgerror)
    print(ioe.diag.message_detail)
    sys.exit(1)

app.config['CORS_HEADERS'] = 'Content-Type'

CORS(app, 
     origins="http://localhost:5000", 
     allow_headers=[
        "Content-Type", 
        "Authorization", 
        "Access-Control-Allow-Credentials",
        "Access-Control-Allow-Origin"
    ],
     supports_credentials=True)

# Create data used to print into the user posts table
user_posts = [
    {"name": "Billy", "secret": "Likes Polka dot patterns, but will never admit it."},
    {"name": "Bobby", "secret": "Thinks Billy needs a shower."},
    {"name": "Lauren", "secret": "Wants John to ask her out"},
    {"name": "John", "secret": "Wants to ask Lauren out, but she's always so cold to him. He's not sure if he should ask her or not."}
]


def Generate_State():
    state = ''.join(random.choice(string.ascii_uppercase + string.digits) for x in range(32))
    login_session['state'] = state


def Is_Authenticated():
    return ('user' in login_session)


def Logout_Session():
    if Is_Authenticated():
        print("Logging out the user")
        login_session.pop('user', None)
        login_session.pop('state', None)



@app.route('/authenticated')
def Authenticated():
    if Is_Authenticated():
        return make_response(jsonify(message="User is already logged in", status=200, data=True))
    else:
        return make_response(jsonify(message="User is not logged in", status=200, data=False))


@app.route('/')
def Index():
    print('Enter Index():')
    Generate_State()

    return render_template(
        'index.html',
        client_id=gAuth.CLIENT_ID,
        authenticated=Is_Authenticated(),
        user_posts=user_posts,
        state=login_session['state']
    )


@app.route('/gconnect', methods=['POST'])
def G_Login():
    print('Enter G_Login()')
    
    if 'state' in request.form:
        if request.form['state'] != login_session['state']:
            return redirect(url_for('Index'))

        if not Is_Authenticated():
            print('Attempt to log in to Google...')
            user_json = gAuth.Google_Callback()

            if user_json:
                user_data = json.loads(user_json)
                
                login_session['user'] = {
                    'name' : user_data['name'],
                    'picture' : user_data['picture'],
                    'email' : user_data['email']
                }

            else:
                Logout_Session()
            
            return make_response(jsonify(
                message="Successfully logged in. Reload the page.",
                status=200,
                data=True
            ))
        else:
            return make_response(jsonify(
                message="Already logged in", 
                status=200,
                data=False
            ))        
    else:
        print('Error: \'state\' is not within the request')

        return redirect(url_for('Index'))


@app.route('/fbconnect', methods=['POST'])
def FB_Login():
    print('Attempting to log in to facebook...')
    
    form = request.form

    if 'state' in form:
        if form['state'] != login_session['state']:
            return make_response(jsonify(
                message='State token does not match.',
                status=401
            ))
        
        user_data = fbAuth.Facebook_Callback(
            form['accessToken'], 
            form['user_id']
        )

        if user_data:
            login_session['user'] = user_data
            
            return make_response(jsonify(
                message="Successfully logged in.",
                status=200,
                data=True
            ))
        else:
            Logout_Session()

            return make_response(jsonify(
                message="User data could not be retrieved.",
                status=401
            ))
    else:
        print('Error: State is not within the request.')

        return make_response(jsonify(
            message="State is not within the request.", 
            status=401
        ))
    
    return make_response(jsonify(
        message="Could not log in user.",
        status=401
    ))
    


@app.route('/fbcallback')
def FB_Callback():
    print('Enter FB_Callback():')
    
    return redirect(url_for('Index'))


@app.route('/logout', methods=['POST'])
def Logout():
    Logout_Session()

    return make_response(jsonify(
        message="User logged out",
        status=200,
        data="Logged Out"
    ))


if __name__ == '__main__':
    context = ('server.crt', 'server.key') #certificate and key files
    app.debug = True
    app.run(
        ssl_context=context,
        host='0.0.0.0',
        port=5000
    )
