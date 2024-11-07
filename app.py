import os

from flask import Flask, jsonify, request, render_template, session, url_for, redirect
from flask_oauthlib.client import OAuth
from flask_pymongo import PyMongo

app = Flask(__name__, template_folder='templates', static_folder='static')
app.secret_key = "110724GAVIN"


# Initialize OAuth
oauth = OAuth(app)

# Configure Google OAuth
google = oauth.remote_app(
    'google',
    consumer_key='46123984513-cggaljds1irlsv3le9avc4li314rla2p.apps.googleusercontent.com',
    consumer_secret='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',
    request_token_params={
        'scope': 'email'
    },
    base_url='https://www.googleapis.com/oauth2/v1/',
    request_token_url=None,
    access_token_method='POST',
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth'
)


@app.route("/")
def hello_world():
    return render_template('index.html')

@app.route('/login')
def login():
    return google.authorize(callback=url_for('index', _external=True))

@app.route('/login/authorized')
def authorized():
    resp = google.authorized_response()
    if resp is None:
        return 'Access denied: reason={} error={}'.format(
            request.args['error_reason'],
            request.args['error_description']
        )
    session['google_token'] = (resp['access_token'], '')
    me = google.get('userinfo')
    return redirect(url_for('index'))

@app.route('/logout')
def logout():
    session.pop('google_token', None)
    return redirect(url_for('index'))

@google.tokengetter
def get_google_oauth_token():
    return session.get('google_token')

if __name__ == "__main__":
    app.run(debug=True)