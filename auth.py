#!/usr/bin/env python
from flask import Flask, abort, request
from uuid import uuid4
import requests
import requests.auth
import urllib
CLIENT_ID = "e9b7d8cc887726ede0fef2aa34aab852"
CLIENT_SECRET = "b4e9b583046cc9844f3aecbbdc20ee58"
REDIRECT_URI = "https://5c968645.ngrok.com/stitch_callback"
 
app = Flask(__name__)
@app.route('/')
def homepage():
    text = '<a href="%s">Authenticate with Stitch</a>'
    return text % make_authorization_url()
 
 
def make_authorization_url():
    state = str(uuid4())
    params = {"client_id": CLIENT_ID,
              "response_type": "code",
              "state": state,
              "redirect_uri": REDIRECT_URI,
              "duration": "temporary"
              }
    url = "https://api.stitchlabs.com/oauth/authorize?" + urllib.urlencode(params)
    return url
 
@app.route('/stitch_callback')
def stitch_callback():
    error = request.args.get('error', '')
    if error:
        return "Error: " + error
    code = request.args.get('code')
    access_token = get_token(code)

    return access_token
 
def get_token(code):
    client_auth = requests.auth.HTTPBasicAuth(CLIENT_ID, CLIENT_SECRET)
    post_data = {"grant_type": "authorization_code",
                 "code": code,
                 "redirect_uri": REDIRECT_URI}
    response = requests.post("https://api.stitchlabs.com/oauth/access_token",
                             auth=client_auth,
                             data=post_data)
    token_json = response.json()
    
    return token_json["access_token"]

def persist_token():
    
    return True

    
@app.route('/orders')
def orders():
    headers = {"Authorization": "Bearer " + _TOKEN_}
    post_data = {"action": "read"}
    response = requests.post("https://api.stitchlabs.com/api2/v2/Products",
                              headers=headers,
                              data=post_data)
    response_json = response.json()
    return "Orders"
    
 
if __name__ == '__main__':
    app.run(debug=True, port=65010)