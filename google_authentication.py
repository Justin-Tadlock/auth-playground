import json

from flask import (
    jsonify,
    request,
    make_response
)

from google.oauth2 import id_token
from google.auth.transport import requests


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

def Authentication_Callback():
    user_data = None

    try:
        # Check if the POST request is trying to log in
        if 'idtoken' in request.form:
            # Get the token from the POST form
            token = request.form['idtoken']

            # Specify the CLIENT_ID of the app that accesses the backend:
            idinfo = id_token.verify_oauth2_token(
                token,
                requests.Request(),
                CLIENT_ID
            )

            verified_providers = [
                'accounts.google.com',
                'https://accounts.google.com'
            ]

            if idinfo['iss'] not in verified_providers:
                raise ValueError('Wrong issuer.')

            # ID token is valid.
            # Get the user's Google Account ID from the decoded token.
            userid = idinfo['sub']

            # Add the token to the flask session variable
            user_data = {
                'name': idinfo['name'],
                'email': idinfo['email'],
                'picture': idinfo['picture']
            }

            ret_response = make_response(
                jsonify(
                    message="Successfully verified token id",
                    status=200,
                    data="Logged In"
                )
            )

    except ValueError:
        # Invalid token
        ret_response = make_response(
            jsonify(message='Error: unable to verify token id', status=401)
        )

    if user_data:
        user_data_json = json.dumps(user_data)
    else:
        user_data_json = None

    return ret_response, user_data_json