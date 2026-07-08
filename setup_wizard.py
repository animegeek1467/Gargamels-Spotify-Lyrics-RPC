from pathlib import Path


APP_DIR = Path(__file__).parent
ENV_PATH = APP_DIR / ".env"

DEFAULT_DISCORD_CLIENT_ID = "1524183156641501334"
DEFAULT_SPOTIFY_CLIENT_ID = "3366681796eb43d1883652a053e215e8"
DEFAULT_SPOTIFY_REDIRECT_URI = "http://127.0.0.1:8888/callback"


def write_env(discord_id, spotify_id, redirect_uri, mode):
    env_content = f"""# Gargamel's Spotify Lyrics RPC
# Mode: {mode}

DISCORD_CLIENT_ID={discord_id}
SPOTIFY_CLIENT_ID={spotify_id}
SPOTIFY_REDIRECT_URI={redirect_uri}
"""

    ENV_PATH.write_text(env_content, encoding="utf8")

    (APP_DIR / "cache" / "lyrics").mkdir(parents=True, exist_ok=True)
    (APP_DIR / "logs").mkdir(parents=True, exist_ok=True)


def easy_mode():
    print()
    print("Easy Mode selected.")
    print("Using Gargamel's default Discord + Spotify app IDs.")
    print("No Spotify Client Secret needed.")
    print()

    write_env(
        DEFAULT_DISCORD_CLIENT_ID,
        DEFAULT_SPOTIFY_CLIENT_ID,
        DEFAULT_SPOTIFY_REDIRECT_URI,
        "Easy"
    )

    print(".env created for Easy Mode.")
    print()
    print("Next:")
    print("1. Open Discord.")
    print("2. Play music on Spotify.")
    print("3. Run START_HERE.bat or run.bat.")


def hard_mode():
    print()
    print("Hard Mode selected.")
    print("Use this if you want your own Discord/Spotify apps.")
    print("Do NOT enter a Spotify Client Secret. This app uses PKCE.")
    print()

    discord_id = input("Discord Application ID: ").strip()
    spotify_id = input("Spotify Client ID: ").strip()

    redirect_uri = input(
        "Spotify Redirect URI [http://127.0.0.1:8888/callback]: "
    ).strip()

    if not redirect_uri:
        redirect_uri = DEFAULT_SPOTIFY_REDIRECT_URI

    if not discord_id.isdigit():
        print()
        print("WARNING: Discord Application ID should only contain numbers.")

    write_env(
        discord_id,
        spotify_id,
        redirect_uri,
        "Hard"
    )

    print()
    print(".env created for Hard Mode.")
    print()
    print("Make sure your Spotify Developer app has this Redirect URI:")
    print(redirect_uri)
    print()
    print("Make sure your Discord Rich Presence asset is named:")
    print("spotify")


def reset_setup():
    print()
    confirm = input("Delete .env and reset setup? Type YES: ").strip()

    if confirm == "YES":
        if ENV_PATH.exists():
            ENV_PATH.unlink()
            print(".env deleted.")
        else:
            print(".env does not exist.")
    else:
        print("Reset cancelled.")


def main():
    print("============================================")
    print("  Gargamel's Spotify Lyrics RPC Setup")
    print("============================================")
    print()
    print("1. Easy Mode")
    print("   Use Gargamel's default app IDs.")
    print("   Best for normal users.")
    print()
    print("2. Hard Mode")
    print("   Use your own Discord + Spotify app IDs.")
    print("   Best for public users or developers.")
    print()
    print("3. Reset setup")
    print()
    print("4. Exit")
    print()

    choice = input("Choose an option: ").strip()

    if choice == "1":
        easy_mode()
    elif choice == "2":
        hard_mode()
    elif choice == "3":
        reset_setup()
    elif choice == "4":
        print("Exiting.")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    main()