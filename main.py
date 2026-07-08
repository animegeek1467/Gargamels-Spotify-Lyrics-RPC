import time

from config import (
    DISCORD_CLIENT_ID,
    INSTRUMENTAL_AFTER_MS,
    INSTRUMENTAL_TEXT,
    NO_LYRICS_TEXT,
    SPOTIFY_POLL_SECONDS,
    SEEK_THRESHOLD_MS,
    NO_PLAYBACK_SLEEP_SECONDS,
    LYRIC_CHECK_SECONDS,
    LYRIC_OFFSET_MS,
    NEXT_LINE_PREVIEW_MS,
    FAST_LINE_GAP_MS,
    MIN_DISCORD_UPDATE_SECONDS,
    CLEAR_ON_PAUSE
)

from spotify_client import SpotifyClient
from lyrics import LyricsClient
from discord_rpc import DiscordRPC
from logger import log


spotify = SpotifyClient()
lyrics = LyricsClient()
rpc = DiscordRPC(DISCORD_CLIENT_ID)

song = None
song_id = None
cached = []

last_poll = 0
sync_time = 0
base_progress = 0
discord_start = int(time.time())

last_lyric = None
last_rpc_update = 0

was_paused = False
no_playback_reported = False


def load_song(current):
    global song_id, cached, discord_start, last_lyric, last_rpc_update

    log("Spotify", f"Now playing: {current['artist']} - {current['name']}")

    cached = lyrics.get_lyrics(
        current["artist"],
        current["name"],
        duration_ms=current["duration_ms"],
        album=current["album"]
    )

    if cached:
        log("Lyrics", f"Loaded {len(cached)} synced lyric lines.")
    else:
        log("Lyrics", NO_LYRICS_TEXT)

    song_id = current["id"]
    last_lyric = None
    last_rpc_update = 0

    discord_start = int(time.time()) - (
        current["progress_ms"] // 1000
    )


def reset_state():
    global song, song_id, cached, last_lyric, was_paused

    song = None
    song_id = None
    cached = []
    last_lyric = None
    was_paused = False


log("App", "Spotify Lyrics RPC started.")

while True:
    now = time.monotonic()

    should_poll_spotify = (
        song is None
        or now - last_poll >= SPOTIFY_POLL_SECONDS
    )

    if should_poll_spotify:
        current = spotify.current_song()
        last_poll = now

        if current is None:
            if not no_playback_reported:
                log("Spotify", "Closed or nothing playing. Clearing Discord.")
                no_playback_reported = True

            rpc.clear()
            reset_state()

            time.sleep(NO_PLAYBACK_SLEEP_SECONDS)
            continue

        no_playback_reported = False

        if not current["is_playing"]:
            if not was_paused:
                log("Spotify", f"Paused: {current['artist']} - {current['name']}")

                if CLEAR_ON_PAUSE:
                    rpc.clear()

                was_paused = True

            song = current
            time.sleep(1)
            continue

        if was_paused:
            log("Spotify", f"Resumed: {current['artist']} - {current['name']}")
            was_paused = False
            last_lyric = None

        predicted_progress = None

        if song is not None and current["id"] == song_id:
            predicted_progress = base_progress + int((now - sync_time) * 1000)

        if current["id"] != song_id:
            load_song(current)

        elif predicted_progress is not None:
            drift = abs(current["progress_ms"] - predicted_progress)

            if drift > SEEK_THRESHOLD_MS:
                log("Spotify", f"Seek detected. Drift: {drift}ms. Resyncing.")
                last_lyric = None
                last_rpc_update = 0
                discord_start = int(time.time()) - (
                    current["progress_ms"] // 1000
                )

        song = current
        base_progress = current["progress_ms"]
        sync_time = now

    if song is not None and not was_paused:
        progress = (
            base_progress
            + int((now - sync_time) * 1000)
            + LYRIC_OFFSET_MS
        )

        if song["duration_ms"]:
            progress = min(progress, song["duration_ms"])

        line = lyrics.current_and_next_line(
            cached,
            progress,
            instrumental_after_ms=INSTRUMENTAL_AFTER_MS,
            instrumental_text=INSTRUMENTAL_TEXT,
            preview_window_ms=NEXT_LINE_PREVIEW_MS,
            fast_line_gap_ms=FAST_LINE_GAP_MS
        )

        if not line and not cached:
            line = NO_LYRICS_TEXT

        if (
            line != last_lyric
            and now - last_rpc_update >= MIN_DISCORD_UPDATE_SECONDS
        ):
            last_lyric = line
            last_rpc_update = now

            log("Lyric", line)

            rpc.update(
                song,
                line,
                discord_start
            )

    time.sleep(LYRIC_CHECK_SECONDS)