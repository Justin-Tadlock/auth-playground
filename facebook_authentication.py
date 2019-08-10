import json

from flask import (
    jsonify,
    request,
    make_response
)

# Get Secrets Data
try:
    SECRET_DATA = json.loads(open('fb_client_secrets.json', 'r').read())['web']
    APP_ID = SECRET_DATA['app_id']
    APP_SECRET = SECRET_DATA['app_secret']

    # Get the redirect uri from the file in the form of '/url'
    CLIENT_REDIRECT = "/oauthcallback"
except:
    print('Error: Could not load the client secrets for the Facebook app.')

def Authentication_Callback():

    return make_response(
        jsonify(message="Test", status=200)
    )