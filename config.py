import os
import sys
from pathlib import Path
from dotenv import load_dotenv


def get_app_dir():
    if getattr(sys, "frozen", False):
        return Path(sys.executable).parent
    return Path(__file__).parent


APP_DIR = get_app_dir()

# Optional .env support.
# Normal users do NOT need .env.
load_dotenv(APP_DIR / ".env", override=True)


# Gargamel's Bot defaults.
# Users can override these in .env, but they do not have to.
DEFAULT_DISCORD_CLIENT_ID = "1524183156641501334"
DEFAULT_SPOTIFY_CLIENT_ID = "3366681796eb43d1883652a053e215e8"
DEFAULT_SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"


DISCORD_CLIENT_ID = (
    os.getenv("DISCORD_CLIENT_ID")
    or DEFAULT_DISCORD_CLIENT_ID
).strip()

SPOTIFY_CLIENT_ID = (
    os.getenv("SPOTIFY_CLIENT_ID")
    or DEFAULT_SPOTIFY_CLIENT_ID
).strip()

SPOTIFY_REDIRECT_URI = (
    os.getenv("SPOTIFY_REDIRECT_URI")
    or DEFAULT_SPOTIFY_REDIRECT_URI
).strip()


MUSIC_EMOJI = "🎵"
LYRIC_EMOJI = "💬"
ARTIST_EMOJI = "👤"
ALBUM_EMOJI = "📀"
BUTTON_EMOJI = "▶"

INSTRUMENTAL_EMOJI = "🎶"
INSTRUMENTAL_TEXT = "Instrumental..."
INSTRUMENTAL_AFTER_MS = 8000

NO_LYRICS_TEXT = "No synced lyrics found"

SPOTIFY_POLL_SECONDS = 2
SEEK_THRESHOLD_MS = 2500
NO_PLAYBACK_SLEEP_SECONDS = 3

LYRIC_CHECK_SECONDS = 0.05
LYRIC_OFFSET_MS = 650

NEXT_LINE_PREVIEW_MS = 1200
FAST_LINE_GAP_MS = 1600
MIN_DISCORD_UPDATE_SECONDS = 0.45

MAX_DETAILS_LENGTH = 128
MAX_STATE_LENGTH = 128
MAX_TEXT_LENGTH = 128

CLEAR_ON_PAUSE = True

DEBUG_LYRICS = False