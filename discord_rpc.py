from pypresence import Presence
from pypresence.types import ActivityType, StatusDisplayType

from config import (
    MUSIC_EMOJI,
    LYRIC_EMOJI,
    ARTIST_EMOJI,
    ALBUM_EMOJI,
    BUTTON_EMOJI,
    INSTRUMENTAL_EMOJI,
    INSTRUMENTAL_TEXT,
    MAX_DETAILS_LENGTH,
    MAX_STATE_LENGTH,
    MAX_TEXT_LENGTH
)

from logger import log


class DiscordRPC:

    def __init__(self, client_id):
        self.client_id = str(client_id).strip()
        self.rpc = None
        self.connected = False

        self.last_details = None
        self.last_state = None
        self.last_large_text = None
        self.last_small_text = None

        self.connect()

    def connect(self):
        try:
            if not self.client_id:
                raise RuntimeError("Missing Discord Client ID.")

            self.rpc = Presence(int(self.client_id))
            self.rpc.connect()
            self.connected = True

            log("Discord", "RPC connected.")

        except Exception as e:
            self.connected = False
            log("Discord", f"RPC not connected: {e}")

    def safe_text(self, text, fallback, max_len=128):
        text = (text or "").strip()

        if len(text) < 2:
            text = fallback

        return text[:max_len]

    def update(self, song, lyric, start):
        if not self.connected:
            self.connect()

        if not self.connected:
            return

        details = self.safe_text(
            f"{MUSIC_EMOJI} {song['name']}",
            "Spotify",
            MAX_DETAILS_LENGTH
        )

        if lyric == INSTRUMENTAL_TEXT:
            state = self.safe_text(
                f"{INSTRUMENTAL_EMOJI} {INSTRUMENTAL_TEXT}",
                "Instrumental",
                MAX_STATE_LENGTH
            )
        else:
            state = self.safe_text(
                f"{LYRIC_EMOJI} {lyric}",
                song["artist"],
                MAX_STATE_LENGTH
            )

        large_text = self.safe_text(
            f"{ALBUM_EMOJI} {song['album']}",
            "Album",
            MAX_TEXT_LENGTH
        )

        small_text = self.safe_text(
            f"{ARTIST_EMOJI} {song['artist']}",
            "Artist",
            MAX_TEXT_LENGTH
        )

        if (
            details == self.last_details
            and state == self.last_state
            and large_text == self.last_large_text
            and small_text == self.last_small_text
        ):
            return

        self.last_details = details
        self.last_state = state
        self.last_large_text = large_text
        self.last_small_text = small_text

        try:
            self.rpc.update(
                activity_type=ActivityType.LISTENING,
                status_display_type=StatusDisplayType.STATE,
                name="Spotify Lyrics",

                details=details,
                state=state,

                large_image="spotify",
                large_text=large_text,
                small_image="spotify",
                small_text=small_text,
                start=start,

                buttons=[
                    {
                        "label": f"{BUTTON_EMOJI} Open in Spotify",
                        "url": song["url"]
                    }
                ]
            )

        except Exception as e:
            log("Discord", f"RPC update error: {e}")
            self.connected = False

    def clear(self):
        if not self.connected:
            return

        try:
            self.rpc.clear()

            self.last_details = None
            self.last_state = None
            self.last_large_text = None
            self.last_small_text = None

            log("Discord", "Status cleared.")

        except Exception as e:
            log("Discord", f"Clear error: {e}")
            self.connected = False