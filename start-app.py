import json
import requests
import httplib2

from flask import (
    Flask, 
    session as login_session,
    redirect, 
    url_for, 
    render_template
)

# Set up the application
app = Flask(__name__)
try:
    app.secret_key = open('secret_key.txt', 'r').read()
except:
    print('Error: Please create a \'secret_key.txt\' file within the app\'s directory')


# Get Secrets Data
try:
    SECRET_DATA = json.loads(open('client_secrets.json', 'r').read())['web']
    CLIENT_ID = SECRET_DATA['client_id']
    CLIENT_SECRET = SECRET_DATA['client_secret']

    # Get the redirect uri from the file in the form of '/url'
    CLIENT_REDIRECT = SECRET_DATA['redirect_uris'][0]
    CLIENT_REDIRECT = '/%s' % (CLIENT_REDIRECT.split('/')[-1])
except:
    print('Error: Please download your \'client_secrets.json\' file from your \'https://console.developers.google.com\' project')


def Is_Authenticated():
    logged_in = False
    if 'user' in login_session:
        logged_in = True
    
    return logged_in

@app.route(CLIENT_REDIRECT)
def Authentication_Callback():
    # Add authentication logic here

    return redirect(url_for('Index'))

@app.route('/')
def Index():
    return render_template('index.html', client_id=CLIENT_ID, logged_in=(Is_Authenticated()))



if __name__ == '__main__':
    app.debug = True
    app.run( 
        host='0.0.0.0', 
        port=5000
    )
