from flask import Flask, request, render_template
from spotify import *

# Start opp spotify-APIet
access_token = get_token()
headers = {
    'Authorization': 'Bearer {token}'.format(token=access_token)
}


app = Flask(__name__)

@app.route("/")
def user_name_form():
    return render_template('user_name_form.html')

@app.route("/", methods = ["POST"])
def playlist_overview():
    # Get user input
    USER_ID = request.form["username"]

    # Get user information from spotify
    user_info = get_user_information(USER_ID, access_token, headers)

    # Get all the users playlists
    playlist = get_user_playlists(USER_ID, access_token, headers)

    return render_template('index.html',
                            user_info = user_info,
                            playlist = playlist)
