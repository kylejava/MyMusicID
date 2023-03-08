import requests
import os
from flask import Flask, render_template, flash, request, redirect
import string
import random
import chardet
import base64
import sys
import pdfkit
app = Flask(__name__)

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
SCOPE = os.environ.get("SCOPE")
ENCODEDSTRING = os.environ.get("ENCODEDSTRING")


@app.route('/' , methods = ['GET' , 'POST'])
def home():
    if(request.method == 'POST'):
        state = string.ascii_lowercase
        state = ''.join(random.choice(state) for i in range(10))
        auth_url = "https://accounts.spotify.com/authorize?response_type=code&redirect_uri={}&scope={}&client_id={}&state={}".format(REDIRECT_URI,SCOPE,CLIENT_ID,state)
        return redirect(auth_url)
    return render_template('index.html')

@app.route('/callback/' , methods = ['GET' , 'POST'])
def callback():
    token = request.args['code']
    state = request.args['state']
    params = {
        "code":token,
        "redirect_uri":REDIRECT_URI,
        "grant_type":"authorization_code"
    }
    HEADERS = {
    "Authorization": "Basic {}".format(ENCODEDSTRING),
    "Content-Type": "application/x-www-form-urlencoded"
    }

    auth_url="https://accounts.spotify.com/api/token"
    requested_data = requests.post(auth_url, data=params, headers = HEADERS)
    final_data = requested_data.json()
    if("error" in final_data):
        return redirect('/')
    return display_data(final_data['access_token'])

@app.route('/display' , methods = ['GET' , 'POST'])
def display_data(my_token):
    profile_picture = "https://thewebinarvet-wordpress.s3.amazonaws.com/uploads/2020/02/spotify-logo.png"
    top_user_songs = []
    top_user_artists = []
    HEADERS = {
        "Authorization" : "Bearer {}".format(my_token),
        "Content-Type":"application.json"
    }
    username = requests.get("https://api.spotify.com/v1/me",headers=HEADERS)
    username = username.json()
    if(len(username["images"]) != 0):
        profile_picture = username["images"][0]["url"]
    user = username['display_name']
    user_id = str(username["id"])
    user_followers = username["followers"]["total"]
    user_link = username["external_urls"]["spotify"]

    user_ = requests.get("https://api.spotify.com/v1/me/top/tracks?time_range=long_term&limit=20&offset=0", headers=HEADERS)
    user_ = user_.json()
    for song in user_["items"]:
        track = u'{}'.format(song["name"])
        print(track)
        artist = song["album"]["artists"][0]["name"]
        top_user_songs.append(track + " - " + artist)
        if(len(top_user_songs) >= 3):
            break

    user_ = requests.get("https://api.spotify.com/v1/me/top/artists?time_range=long_term&limit=20&offset=0", headers=HEADERS)
    user_ = user_.json()
    for song in user_["items"]:
        artists = u'{}'.format(song["name"])
        top_user_artists.append(artists)
        if(len(top_user_artists) >= 3):
            break
    data = {
        "profile_picture":str(profile_picture),
        "username":str(user),
        "user_id":str(user_id),
        "user_followers":str(user_followers),
        "top_user_songs":(top_user_songs),
        "user_link":str(user_link),
        "top_user_artists":(top_user_artists)
    }
    return render_template("result.html", data=data)



@app.route('/test', methods=['GET','POST'])
def test():
    return render_template('result.html')

if __name__ == "__main__":
    app.run(debug=True)
