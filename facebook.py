from flask import Flask, redirect, url_for, session, request
from flask_oauthlib.client import OAuth, OAuthException

FACEBOOK_APP_ID = '1465823483485054'
FACEBOOK_APP_SECRET = '33bc57bcdae3b43356b826409ec1590e'

oauth = OAuth()
facebook = oauth.remote_app(
        'facebook',
        consumer_key=FACEBOOK_APP_ID,
        consumer_secret=FACEBOOK_APP_SECRET,
        request_token_params={'scope': 'email'},
        base_url='https://graph.facebook.com',
        request_token_url=None,
        access_token_url='/oauth/access_token',
        access_token_method='GET',
        authorize_url='https://www.facebook.com/dialog/oauth'
    )

def init_fb(app):
    oauth.init_app(app)

@facebook.tokengetter
def get_facebook_oauth_token():
    return session.get('oauth_token')


