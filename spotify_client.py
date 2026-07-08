import spotipy
from spotipy.oauth2 import SpotifyPKCE

from config import (
    APP_DIR,
    SPOTIFY_CLIENT_ID,
    SPOTIFY_REDIRECT_URI
)

from logger import log


SCOPE = "user-read-currently-playing user-read-playback-state"


class SpotifyClient:

    def __init__(self):
        if not SPOTIFY_CLIENT_ID:
            raise RuntimeError("Missing Spotify Client ID.")

        if not SPOTIFY_REDIRECT_URI:
            raise RuntimeError("Missing Spotify Redirect URI.")

        self.spotify = spotipy.Spotify(
            auth_manager=SpotifyPKCE(
                client_id=SPOTIFY_CLIENT_ID,
                redirect_uri=SPOTIFY_REDIRECT_URI,
                scope=SCOPE,
                open_browser=True,
                cache_path=str(APP_DIR / ".spotifycache")
            )
        )

    def current_song(self):
        try:
            playback = self.spotify.current_playback()

            if playback is None:
                return None

            item = playback.get("item")

            if item is None:
                return None

            if item.get("type") != "track":
                return None

            album = item.get("album") or {}
            album_images = album.get("images") or []

            image = ""
            if album_images:
                image = album_images[0].get("url", "")

            external_urls = item.get("external_urls") or {}

            return {
                "id": item.get("id"),
                "name": item.get("name", "Unknown Song"),
                "artist": ", ".join(
                    a.get("name", "Unknown Artist")
                    for a in item.get("artists", [])
                ),
                "album": album.get("name", "Unknown Album"),
                "duration_ms": item.get("duration_ms", 0),
                "progress_ms": playback.get("progress_ms", 0),
                "is_playing": playback.get("is_playing", False),
                "image": image,
                "url": external_urls.get("spotify", "https://open.spotify.com")
            }

        except Exception as e:
            log("Spotify", f"Error: {e}")
            return None