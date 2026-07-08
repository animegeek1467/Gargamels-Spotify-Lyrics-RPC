# 🎵 Gargamel's Spotify Lyrics RPC

A Discord Rich Presence app that shows your current Spotify song and live synced lyrics.

## Quick Start

1. Download the ZIP.
2. Extract it.
3. Open Discord.
4. Play something on Spotify.
5. Double-click `START_HERE.bat`.
6. Pick Easy Mode.
7. Log into Spotify when your browser opens.
8. Done.

---

# Easy Guide

Use this if you just want it working.

1. Double-click `START_HERE.bat`.
2. Choose `1. Easy Mode`.
3. Let it install requirements.
4. Log into Spotify.
5. Your Discord status should update.

No Discord Developer setup.
No Spotify Client Secret.
No manual `.env` editing.

Note: Easy Mode uses Gargamel's default Spotify app. If Spotify blocks login, use Hard Mode.

---

# Hard Guide

Use this if Easy Mode does not work or if you want your own app IDs.

## Discord

1. Go to Discord Developer Portal.
2. Create an application.
3. Copy the Application ID.
4. Go to Rich Presence Art Assets.
5. Upload an image named `spotify`.

## Spotify

1. Go to Spotify Developer Dashboard.
2. Create an app.
3. Copy the Client ID.
4. Add this Redirect URI:

http://127.0.0.1:8888/callback

5. Save.

## Setup

1. Double-click `START_HERE.bat`.
2. Choose `2. Hard Mode`.
3. Paste your Discord Application ID.
4. Paste your Spotify Client ID.
5. Use the default redirect URI.
6. Run the app.

Do not enter or share a Spotify Client Secret. This app uses PKCE.

---

# Troubleshooting

## Discord only shows the app name

Restart Discord and restart the bot.

## Spotify login fails

Make sure your Redirect URI is exactly:

http://127.0.0.1:8888/callback

## Lyrics do not show

LRCLIB may not have synced lyrics for that song.

## Fast rap is delayed

Discord Rich Presence cannot perfectly update ultra-fast lyrics. Try changing `LYRIC_OFFSET_MS` in `config.py`.

---

# Do Not Upload

Never upload:

.env
.spotifycache
cache/
logs/
__pycache__/