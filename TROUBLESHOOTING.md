# 🛠 Gargamel's Spotify Lyrics RPC Troubleshooting Guide

This guide covers common problems and how to fix them.

Most issues are caused by one of these:

- Spotify auth cache bug
- Discord not open
- Missing Python packages
- Bad `.env`
- Lyrics not available
- Discord RPC update limits

---

## 1. Spotify keeps saying `invalid_request`

### Error example

```txt
[Spotify] Error: error: invalid_request, error_description:
[Discord] Status cleared.
```

### Cause

Spotify’s saved login cache got corrupted, expired, or was created with an older auth method.

### Fix

Close the bot with:

```txt
Ctrl + C
```

Then delete this file from the project folder:

```txt
.spotifycache
```

If you see this file too, delete it:

```txt
.cache
```

Then run:

```txt
START_HERE.bat
```

Spotify should open in your browser again. Log in and approve the app.

---

## 2. Permanent Spotify cache fix

If `invalid_request` keeps coming back, open `spotify_client.py`.

Find:

```python
cache_path=str(APP_DIR / ".spotifycache")
```

Change it to:

```python
cache_path=str(APP_DIR / ".gargamel_spotify_cache")
```

Then delete the old file:

```txt
.spotifycache
```

Run the bot again.

---

## 3. Discord RPC not connected

### Error example

```txt
[Discord] RPC not connected
```

### Fix checklist

Make sure:

- Discord desktop app is open
- You are logged into Discord
- You are not using only Discord in browser
- Your Discord app ID is valid
- Your internet is working

Then restart:

```txt
run.bat
```

If it still fails, fully close Discord from the system tray and reopen it.

---

## 4. Discord only shows the app name

### Problem

Discord only shows:

```txt
Spotify Lyrics RPC
```

instead of the lyric.

### Fix

Restart Discord.

Discord sometimes caches Rich Presence display data.

Also make sure `discord_rpc.py` has this inside `self.rpc.update(...)`:

```python
activity_type=ActivityType.LISTENING,
status_display_type=StatusDisplayType.STATE,
name="Spotify Lyrics",
```

---

## 5. `Client ID is invalid`

### Cause

The Discord Client ID is missing, wrong, or has spaces/quotes.

### Fix

If using Easy Mode, rerun:

```txt
START_HERE.bat
```

Choose:

```txt
1. Easy Mode
```

If using Hard Mode, check `.env`.

Correct:

```env
DISCORD_CLIENT_ID=1234567890123456789
```

Wrong:

```env
DISCORD_CLIENT_ID = 1234567890123456789
DISCORD_CLIENT_ID="1234567890123456789"
```

No quotes.  
No spaces around `=`.

---

## 6. Spotify login does not open

### Fix

Run this first:

```txt
install_requirements.bat
```

Then run:

```txt
START_HERE.bat
```

If it still does not open, check that your browser is not blocking popups.

---

## 7. Spotify login opens but fails

### Hard Mode users

Make sure your Spotify Redirect URI is exactly:

```txt
http://127.0.0.1:8888/callback
```

It must match in both:

- Spotify Developer Dashboard
- `.env`

Correct:

```env
SPOTIFY_REDIRECT_URI=http://127.0.0.1:8888/callback
```

Do not use:

```txt
localhost
```

Use:

```txt
127.0.0.1
```

---

## 8. Easy Mode Spotify login fails

Easy Mode uses Gargamel’s default Spotify app.

If Spotify blocks login, the app may need your Spotify account added to the allowlist, or you need to use Hard Mode.

### Fix

Run:

```txt
START_HERE.bat
```

Choose:

```txt
2. Hard Mode
```

Then use your own Spotify Client ID.

You do **not** need a Spotify Client Secret.

---

## 9. Lyrics do not show

### Possible causes

- LRCLIB does not have synced lyrics for that song
- Song title is weirdly formatted
- The wrong lyric version was found
- The track is too new
- The track is a remix/live/sped-up version

### Fix

Try another popular song first.

If only one song is broken, delete its cached lyric file from:

```txt
cache/lyrics/
```

Then restart the bot.

---

## 10. It says `Instrumental...` forever

### Cause

The lyric file may have bad timestamps, blank lyric lines, or the wrong version was cached.

### Fix

Delete the song’s cached file in:

```txt
cache/lyrics/
```

Then restart:

```txt
run.bat
```

If it still happens, LRCLIB probably does not have a good synced lyric file for that song.

---

## 11. Fast rap feels delayed

Discord Rich Presence is not built for ultra-fast karaoke updates.

For fast songs, edit `config.py`:

```python
LYRIC_CHECK_SECONDS = 0.05
LYRIC_OFFSET_MS = 650
NEXT_LINE_PREVIEW_MS = 1200
FAST_LINE_GAP_MS = 1600
MIN_DISCORD_UPDATE_SECONDS = 0.45
```

If lyrics are late:

```python
LYRIC_OFFSET_MS = 800
```

If lyrics are too early:

```python
LYRIC_OFFSET_MS = 450
```

Some songs are simply too fast for Discord RPC to display perfectly.

---

## 12. The bot worked, then randomly stopped

Try this order:

1. Close the bot with `Ctrl + C`
2. Delete:

```txt
.spotifycache
```

3. Run:

```txt
run.bat
```

If still broken:

4. Delete:

```txt
cache/lyrics/
logs/
```

5. Run:

```txt
START_HERE.bat
```

---

## 13. `ModuleNotFoundError`

### Error example

```txt
ModuleNotFoundError: No module named 'spotipy'
```

### Fix

Run:

```txt
install_requirements.bat
```

Or run:

```powershell
python -m pip install -r requirements.txt
```

Then start again:

```txt
run.bat
```

---

## 14. Python not found

### Error example

```txt
Python was not found
```

### Fix

Install Python from:

```txt
https://www.python.org/downloads/
```

During install, check:

```txt
Add Python to PATH
```

Then restart your PC or reopen the terminal.

---

## 15. Bot closes instantly

Do not double-click `main.py`.

Use:

```txt
START_HERE.bat
```

or:

```txt
run.bat
```

These keep the window open so you can see errors.

---

## 16. Discord status does not clear after pause

Check `config.py`.

If you want Discord to clear when paused:

```python
CLEAR_ON_PAUSE = True
```

If you want it to stay visible:

```python
CLEAR_ON_PAUSE = False
```

---

## 17. Spotify is playing but bot says nothing is playing

Try:

1. Make sure Spotify is actually playing, not paused.
2. Skip to another song.
3. Restart Spotify.
4. Restart the bot.
5. Delete `.spotifycache` and log in again.

---

## 18. Clean reset

Use this if everything feels broken.

Close the bot.

Delete:

```txt
.env
.spotifycache
.gargamel_spotify_cache
cache/
logs/
__pycache__/
```

Then run:

```txt
START_HERE.bat
```

Pick Easy Mode or Hard Mode again.

---

## 19. Files you should never upload

Do not upload:

```txt
.env
.spotifycache
.gargamel_spotify_cache
cache/
logs/
__pycache__/
```

These may contain personal login/session data or local files.

---

## 20. Best fix order

If something breaks, try this order:

```txt
1. Restart Discord
2. Restart Spotify
3. Restart the bot
4. Delete .spotifycache
5. Delete cache/lyrics
6. Run START_HERE.bat again
7. Use Hard Mode if Easy Mode login fails
```

---

## Still broken?

Send the full terminal error.

Do not just say “it broke.”

Include:

```txt
What song was playing?
Were you using Easy Mode or Hard Mode?
Did Discord open?
Did Spotify login open?
Full error text
Screenshot if possible
```