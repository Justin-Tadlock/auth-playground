import json
import httplib2
import sys

from flask import (
    jsonify,
    request,
    make_response
)

import facebook

# Get Secrets Data
try:
    SECRET_DATA = json.loads(open('fb_client_secrets.json', 'r').read())['web']
    APP_ID = SECRET_DATA['app_id']
    APP_SECRET = SECRET_DATA['app_secret']

    # Get the redirect uri from the file in the form of '/url'
    CLIENT_REDIRECT = "/oauthcallback"
except IOError as ioe:
    print('Error: Could not load the client secrets for the Facebook app.')
    print(ioe.pgerror)
    print(ioe.diag.message_detail)
    sys.exit(1)


def Facebook_Callback(access_token, user_id):
    print('Enter Facebook_Callback()')

    graph_api = facebook.GraphAPI(access_token)

    if graph_api:
        user_json = graph_api.get_object('me', fields="name,email")

        if user_json:
            user_data = user_json
            user_data['accessToken'] = access_token
        else:
            user_data = None

    return user_data
