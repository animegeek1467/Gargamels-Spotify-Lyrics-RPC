@echo off
cd /d "%~dp0"

set "RPC_TARGET=%~dp0run.bat"
set "RPC_DIR=%~dp0"

powershell -NoProfile -ExecutionPolicy Bypass -Command "$W=New-Object -ComObject WScript.Shell; $S=$W.CreateShortcut($env:APPDATA + '\Microsoft\Windows\Start Menu\Programs\Startup\Spotify Lyrics RPC.lnk'); $S.TargetPath=$env:RPC_TARGET; $S.WorkingDirectory=$env:RPC_DIR; $S.Save()"

echo Spotify Lyrics RPC added to Windows startup.
pause