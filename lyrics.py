import json
import re
import bisect
import unicodedata
from pathlib import Path
from difflib import SequenceMatcher

import requests

from config import (
    APP_DIR,
    INSTRUMENTAL_TEXT,
    DEBUG_LYRICS
)

from logger import log


CACHE_DIR = APP_DIR / "cache" / "lyrics"
CACHE_DIR.mkdir(parents=True, exist_ok=True)


class LyricsClient:

    def __init__(self):
        self.memory = {}

    def normalize(self, text):
        text = text or ""
        text = unicodedata.normalize("NFKD", text)
        text = text.encode("ascii", "ignore").decode("ascii")
        text = text.lower()

        text = re.sub(r"\(feat\..*?\)", "", text)
        text = re.sub(r"\(ft\..*?\)", "", text)
        text = re.sub(r"\[feat\..*?\]", "", text)
        text = re.sub(r"\[ft\..*?\]", "", text)

        text = re.sub(r"[^a-z0-9 ]+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()

        return text

    def ratio(self, a, b):
        a = self.normalize(a)
        b = self.normalize(b)

        if not a or not b:
            return 0

        return SequenceMatcher(None, a, b).ratio()

    def first_artist(self, artist):
        if not artist:
            return ""

        return artist.split(",")[0].strip()

    def safe_filename(self, artist, title, duration_ms=None):
        name = f"{artist}-{title}"

        if duration_ms:
            name += f"-{duration_ms}"

        name = re.sub(r'[<>:"/\\|?*]', "_", name)
        return name.lower() + ".json"

    def cache_path(self, artist, title, duration_ms=None):
        return CACHE_DIR / self.safe_filename(artist, title, duration_ms)

    def get_lyrics(self, artist, title, duration_ms=None, album=None):
        key = f"{artist}-{title}-{duration_ms}".lower()

        if key in self.memory:
            return self.memory[key]

        path = self.cache_path(artist, title, duration_ms)

        if path.exists():
            try:
                with open(path, "r", encoding="utf8") as f:
                    lyrics = json.load(f)

                self.memory[key] = lyrics
                return lyrics

            except Exception:
                pass

        results = self.search_lrclib(artist, title)

        if not results:
            log("Lyrics", "No LRCLIB results found.")
            self.memory[key] = []
            return []

        best = self.pick_best_result(
            results=results,
            artist=artist,
            title=title,
            duration_ms=duration_ms,
            album=album
        )

        if best is None:
            log("Lyrics", "No synced lyrics found.")
            self.memory[key] = []
            return []

        synced_lrc = best.get("syncedLyrics")

        if not synced_lrc:
            log("Lyrics", "Best result had no synced lyrics.")
            self.memory[key] = []
            return []

        parsed = self.parse_lrc(synced_lrc)

        try:
            with open(path, "w", encoding="utf8") as f:
                json.dump(parsed, f)
        except Exception:
            pass

        self.memory[key] = parsed
        return parsed

    def search_lrclib(self, artist, title):
        try:
            response = requests.get(
                "https://lrclib.net/api/search",
                params={
                    "artist_name": artist,
                    "track_name": title
                },
                headers={
                    "User-Agent": "SpotifyLyricsRPC/2.0"
                },
                timeout=10
            )

            if response.status_code != 200:
                log("Lyrics", f"LRCLIB returned status {response.status_code}")
                return []

            return response.json()

        except Exception as e:
            log("Lyrics", f"Search error: {e}")
            return []

    def pick_best_result(self, results, artist, title, duration_ms=None, album=None):
        best = None
        best_score = -1

        spotify_duration_seconds = None

        if duration_ms:
            spotify_duration_seconds = duration_ms / 1000

        for item in results:
            synced = item.get("syncedLyrics")

            if not synced:
                continue

            result_title = item.get("trackName") or item.get("name") or ""
            result_artist = item.get("artistName") or ""
            result_album = item.get("albumName") or ""
            result_duration = item.get("duration")

            title_score = self.ratio(title, result_title)

            artist_score = max(
                self.ratio(artist, result_artist),
                self.ratio(self.first_artist(artist), result_artist)
            )

            album_score = self.ratio(album or "", result_album) if album else 0

            duration_score = 0

            if spotify_duration_seconds and result_duration:
                diff = abs(float(result_duration) - spotify_duration_seconds)

                if diff <= 1:
                    duration_score = 1
                elif diff <= 3:
                    duration_score = 0.85
                elif diff <= 6:
                    duration_score = 0.6
                elif diff <= 10:
                    duration_score = 0.3
                else:
                    duration_score = 0

            score = (
                title_score * 0.45
                + artist_score * 0.30
                + album_score * 0.10
                + duration_score * 0.15
            )

            if DEBUG_LYRICS:
                log(
                    "Lyrics",
                    f"Candidate: {result_artist} - {result_title} | score={score:.3f}"
                )

            if score > best_score:
                best = item
                best_score = score

        if best:
            log(
                "Lyrics",
                f"Best match: {best.get('artistName')} - {best.get('trackName')} | score={best_score:.3f}"
            )

        return best

    def parse_lrc(self, lrc):
        parsed = []

        for line in lrc.splitlines():
            timestamps = re.findall(r"\[(\d+):(\d+(?:\.\d+)?)\]", line)

            if not timestamps:
                continue

            lyric = re.sub(r"\[(\d+):(\d+(?:\.\d+)?)\]", "", line).strip()

            for minute, second in timestamps:
                timestamp_ms = int((int(minute) * 60 + float(second)) * 1000)
                parsed.append([timestamp_ms, lyric])

        parsed.sort(key=lambda x: x[0])
        return parsed

    def get_index(self, lyrics, progress_ms):
        if not lyrics:
            return -1

        timestamps = [line[0] for line in lyrics]
        return bisect.bisect_right(timestamps, progress_ms) - 1

    def current_line(
        self,
        lyrics,
        progress_ms,
        instrumental_after_ms=8000,
        instrumental_text=INSTRUMENTAL_TEXT
    ):
        if not lyrics:
            return ""

        index = self.get_index(lyrics, progress_ms)

        if index < 0:
            return instrumental_text

        current_timestamp, current_lyric = lyrics[index]
        current_lyric = (current_lyric or "").strip()

        if not current_lyric:
            return instrumental_text

        if index + 1 < len(lyrics):
            next_timestamp = lyrics[index + 1][0]

            gap_to_next = next_timestamp - current_timestamp
            time_on_current = progress_ms - current_timestamp

            if (
                gap_to_next >= instrumental_after_ms
                and time_on_current >= instrumental_after_ms
            ):
                return instrumental_text

        else:
            time_on_current = progress_ms - current_timestamp

            if time_on_current >= instrumental_after_ms:
                return instrumental_text

        return current_lyric

    def current_and_next_line(
        self,
        lyrics,
        progress_ms,
        instrumental_after_ms=8000,
        instrumental_text=INSTRUMENTAL_TEXT,
        preview_window_ms=1200,
        fast_line_gap_ms=1600
    ):
        current = self.current_line(
            lyrics,
            progress_ms,
            instrumental_after_ms=instrumental_after_ms,
            instrumental_text=instrumental_text
        )

        if not lyrics:
            return current

        if not current or current == instrumental_text:
            return current

        index = self.get_index(lyrics, progress_ms)

        if index < 0:
            return current

        if index + 1 >= len(lyrics):
            return current

        current_timestamp = lyrics[index][0]
        next_timestamp, next_lyric = lyrics[index + 1]
        next_lyric = (next_lyric or "").strip()

        if not next_lyric:
            return current

        gap_to_next = next_timestamp - current_timestamp
        time_until_next = next_timestamp - progress_ms

        if (
            0 <= time_until_next <= preview_window_ms
            and gap_to_next <= fast_line_gap_ms
        ):
            return f"{current} / {next_lyric}"

        return current