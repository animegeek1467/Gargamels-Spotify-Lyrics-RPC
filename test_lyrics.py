from spotify_client import SpotifyClient
from lyrics import LyricsClient
import time

spotify = SpotifyClient()
lyrics = LyricsClient()

song = None
song_id = None
cached = []

last_poll = 0
sync_time = 0
base_progress = 0

while True:

    now = time.monotonic()

    if song is None or now - last_poll >= 10:

        current = spotify.current_song()

        if current is not None:

            if current["id"] != song_id:

                print(f"\nLoading: {current['artist']} - {current['name']}")

                cached = lyrics.get_lyrics(
                    current["artist"],
                    current["name"]
                )

                print(f"Loaded {len(cached)} lyric lines")

                song_id = current["id"]

            song = current
            base_progress = current["progress_ms"]
            sync_time = now

        last_poll = now

    if song:

        progress = base_progress + int((now - sync_time) * 1000)

        line = lyrics.current_line(cached, progress)

        print(line)

    time.sleep(1)