from flask import Flask, redirect, request, jsonify, session, render_template
import requests
from datetime import datetime
import os
import urllib.parse
import json

from chatgpt import get_ai_response

app = Flask(__name__)

# Secret key for session management
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "default_key")

# Spotify API configuration
CLIENT_ID = os.environ.get("SPOTIFY_CLIENT_ID")
CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
REDIRECT_URI = "http://localhost:5000/callback"
AUTH_URL = "https://accounts.spotify.com/authorize"
TOKEN_URL = "https://accounts.spotify.com/api/token"
API_BASE_URL = "https://api.spotify.com/v1/"


def send_spotify_request(method, endpoint, headers=None, params=None, data=None):
    """Helper function to send requests to Spotify API."""
    url = f"{API_BASE_URL}{endpoint}"
    response = requests.request(method, url, headers=headers, params=params, json=data)
    if response.status_code not in range(200, 300):
        response.raise_for_status()
    return response.json()


def refresh_access_token():
    """Refresh the Spotify access token using the refresh token."""
    if "refresh_token" not in session:
        return redirect("/login")

    req_body = {
        "grant_type": "refresh_token",
        "refresh_token": session["refresh_token"],
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET,
    }
    response = requests.post(TOKEN_URL, data=req_body).json()

    if "access_token" in response:
        session["access_token"] = response["access_token"]
        session["expires_at"] = datetime.now().timestamp() + response["expires_in"]
    else:
        session.clear()
        return redirect("/login")


def is_token_expired():
    """Check if the access token has expired."""
    return datetime.now().timestamp() > session.get("expires_at", 0)


def ensure_authenticated():
    """Ensure the user is authenticated, refreshing token if necessary."""
    if "access_token" not in session or is_token_expired():
        refresh_access_token()


@app.route("/")
def index():
    if not session.get("authenticated"):
        return render_template("login.html")
    return render_template("index.html")


@app.route("/login")
def login():
    scope = "user-read-private user-read-email user-top-read user-read-recently-played playlist-modify-public playlist-modify-private"
    params = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "show_dialog": True,
    }
    auth_url = f"{AUTH_URL}?{urllib.parse.urlencode(params)}"
    return redirect(auth_url)


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")


@app.route("/callback")  # type: ignore
def callback():
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})

    if "code" in request.args:
        req_body = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        token_info = requests.post(TOKEN_URL, data=req_body).json()
        session["access_token"] = token_info["access_token"]
        session["refresh_token"] = token_info["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]
        session["authenticated"] = True
        return redirect("/")


@app.route("/playlists")
def get_playlists():
    ensure_authenticated()
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    playlists = send_spotify_request("GET", "me/playlists", headers=headers)
    return jsonify(playlists)


@app.route("/top-tracks")
def get_top_tracks():
    ensure_authenticated()
    # print(session)
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    tracks_info = send_spotify_request(
        "GET", "me/top/tracks", headers=headers, params={"limit": 20, "market": "IN"}
    )
    # print(tracks_info)
    # with open("tracks.json", "w") as f:
    #     json.dump(tracks_info, f)
    tracks = [
        {
            "track_name": item["name"],
            "artist_name": item["artists"][0]["name"],
            "album_image": item["album"]["images"][0]["url"],
            "uri": item["uri"],
        }
        for item in tracks_info["items"]
    ]
    return render_template("top_track.html", tracks=tracks)


@app.route("/favorite-artist")
def favorite_artists():
    ensure_authenticated()
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = send_spotify_request(
        "GET", "me/top/artists", headers=headers, params={"limit": 20}
    )

    def format_followers(count):
        if count >= 1_000_000:
            return f"{count // 1_000_000}M"
        elif count >= 1_000:
            return f"{count // 1_000}K"
        return str(count)

    def categorize_popularity(score):
        if score >= 80:
            return "Legend 🌟"
        elif score >= 60:
            return "Superstar"
        elif score >= 40:
            return "Popular"
        elif score >= 20:
            return "Rising Star"
        return "Emerging Artist"

    favorite_artists = [
        {
            "rank": idx + 1,
            "name": artist["name"],
            "popularity": categorize_popularity(artist["popularity"]),
            "genres": ", ".join(artist["genres"]),
            "followers": format_followers(artist["followers"]["total"]),
            "image": artist["images"][0]["url"],
        }
        for idx, artist in enumerate(response["items"])
    ]
    return render_template("favorite_artist.html", favorite_artists=favorite_artists)


@app.route("/genie")
def genie():
    ensure_authenticated()
    headers = {"Authorization": f"Bearer {session['access_token']}"}
    response = send_spotify_request(
        "GET", "me/top/tracks", headers=headers, params={"limit": 20}
    )

    tracks = [
        {
            "track_name": item["name"],
            "artist_name": item["artists"][0]["name"],
            # "album_image": item["album"]["images"][0]["url"],
            # "uri": item["uri"],
        }
        for item in response["items"]
    ]

    response = get_ai_response.invoke({"songs": tracks, "name": "Samriddhi"})
    print(response)
    return render_template("chatgpt.html", analysis=response["analysis"])


@app.route("/create-playlist")
def create_playlist():
    ensure_authenticated()
    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Content-Type": "application/json",
    }

    user_profile = send_spotify_request("GET", "me", headers=headers)
    user_id = user_profile.get("id")
    if not user_id:
        return jsonify({"error": "User ID not found"}), 400

    playlist_data = {
        "name": "Top 20 songs",
        "description": "A list of my top 20 Spotify tracks",
        "public": True,
    }

    playlist = send_spotify_request(
        "POST", f"users/{user_id}/playlists", headers=headers, data=playlist_data
    )
    return redirect(f"/add-tracks/{playlist['id']}")


@app.route("/add-tracks/<playlist_id>")
def add_tracks(playlist_id):
    ensure_authenticated()
    headers = {
        "Authorization": f"Bearer {session['access_token']}",
        "Content-Type": "application/json",
    }

    top_tracks = send_spotify_request(
        "GET", "me/top/tracks", headers=headers, params={"limit": 20}
    )
    track_uris = [item["uri"] for item in top_tracks["items"]]

    send_spotify_request(
        "POST",
        f"playlists/{playlist_id}/tracks",
        headers=headers,
        data={"uris": track_uris},
    )
    return redirect(f"/view-playlist/{playlist_id}")


@app.route("/view-playlist/<playlist_id>")
def view_playlist(playlist_id):
    ensure_authenticated()
    headers = {"Authorization": f"Bearer {session['access_token']}"}

    playlist_data = send_spotify_request(
        "GET", f"playlists/{playlist_id}", headers=headers
    )
    tracks_data = send_spotify_request(
        "GET", f"playlists/{playlist_id}/tracks", headers=headers
    )

    tracks = [
        {
            "name": track["track"]["name"],
            "artist": track["track"]["artists"][0]["name"],
            "album": track["track"]["album"]["name"],
            "image": (
                track["track"]["album"]["images"][0]["url"]
                if track["track"]["album"]["images"]
                else None
            ),
            "preview_url": track["track"]["preview_url"],
        }
        for track in tracks_data["items"]
    ]

    return render_template(
        "view_playlist.html",
        playlist_name=playlist_data["name"],
        playlist_description=playlist_data["description"],
        tracks=tracks,
        spotify_url=playlist_data["external_urls"]["spotify"],
    )


if __name__ == "__main__":
    app.run(debug=True)
