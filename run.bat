@echo off
cd /d "%~dp0"

title Gargamel's Spotify Lyrics RPC

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    set "PYTHON_CMD=py -3"
) else (
    set "PYTHON_CMD=python"
)

%PYTHON_CMD% -u main.py

echo.
echo App stopped or crashed.
pause