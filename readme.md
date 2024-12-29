# Tune Stats

Tune Stats is a web application that allows users to analyze their Spotify listening habits. Users can view their top tracks, favorite artists, and detailed track analysis. The application also allows users to create playlists based on their top tracks.

## Features

- **Login with Spotify**: Authenticate users using their Spotify account.
- **Top Tracks**: Display the user's top 20 tracks.
- **Favorite Artists**: Display the user's favorite artists with detailed information.
- **Create Playlist**: Create a playlist of the user's top 20 tracks on Spotify.
- **Spotify Genie**: Generate a personalized analysis using AI.

## Project Structure

```
.
├── __pycache__/
├── app.py
├── chatgpt.py
├── static/
│   ├── css/
│   │   ├── chatgpt.css
│   │   ├── favorite_artist.css
│   │   ├── index.css
│   │   ├── login.css
│   │   ├── top_track.css
│   │   ├── track_analysis.css
│   │   └── view_playlist.css
│   ├── images/
├── templates/
│   ├── chatgpt.html
│   ├── favorite_artist.html
│   ├── index.html
│   ├── login.html
│   ├── top_track.html
│   ├── track_analysis.html
│   └── view_playlist.html
├── tracks.json
└── test.py
```

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/yourusername/tune-stats.git
    cd tune-stats
    ```

2. Install the required dependencies:
    ```sh
    pip install -r requirements.txt
    ```

3. Set up environment variables:
    ```sh
    export CLIENT_ID="your_spotify_client_id"
    export CLIENT_SECRET="your_spotify_client_secret"
    export SECRET_KEY="your_flask_secret_key"
    ```

4. Run the application:
    ```sh
    python app.py
    ```

## Usage

1. Open your browser and navigate to `http://localhost:5000`.
2. Click on "Login with Spotify" to authenticate.
3. Explore the various features:
    - **Top Tracks**: View your top 20 tracks.
    - **Favorite Artists**: View your favorite artists.
    - **Track Analysis**: Analyze the audio features of your tracks.
    - **Create Playlist**: Create a playlist of your top 20 tracks.
    - **Spotify Genie**: Get a personalized analysis using AI.

## File Descriptions

- **app.py**: Main application file containing route definitions and Spotify API interactions.
- **chatgpt.py**: Contains the function to get AI responses.
- **static/**: Contains static files such as CSS and JavaScript.
- **templates/**: Contains HTML templates for rendering the web pages.
- **tracks.json**: Stores the user's top tracks information.
- **test.py**: Contains test scripts for various functionalities.

## Screenshots

![image](https://github.com/user-attachments/assets/4d240b4a-8ded-43f1-85d6-0c3a00e7f100)

## Routes

- `/`: Home page.
- `/login`: Login page.
- `/logout`: Logout and clear session.
- `/callback`: Spotify OAuth callback.
- `/playlists`: Get user's playlists.
- `/top-tracks`: Display user's top tracks.
- `/favorite-artist`: Display user's favorite artists.
- `/track-analysis`: Display track analysis.
- `/genie`: Generate personalized analysis using AI.
- `/create-playlist`: Create a playlist of top tracks.
- `/add-tracks/<playlist_id>`: Add tracks to a playlist.
- `/view-playlist/<playlist_id>`: View a playlist.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements

- [Spotify Web API](https://developer.spotify.com/documentation/web-api/)
- [Flask](https://flask.palletsprojects.com/)

## Contact

For any questions or feedback, please contact [ssamriddhi47@gmail.com](mailto:ssamriddhi47@gmail.com).
