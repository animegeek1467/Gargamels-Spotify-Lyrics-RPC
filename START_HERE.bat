@echo off
cd /d "%~dp0"

title Gargamel's Spotify Lyrics RPC

echo.
echo ============================================
echo   Gargamel's Spotify Lyrics RPC
echo ============================================
echo.
echo First launch setup.
echo Keep Discord open.
echo Spotify login may open in your browser.
echo.

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    set "PYTHON_CMD=py -3"
) else (
    set "PYTHON_CMD=python"
)

echo Checking Python...
%PYTHON_CMD% --version

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Python was not found.
    echo Install Python from:
    echo https://www.python.org/downloads/
    echo.
    echo Make sure to check:
    echo Add Python to PATH
    echo.
    pause
    exit /b
)

echo.
echo Installing requirements...
%PYTHON_CMD% -m pip install -r requirements.txt

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo Failed to install requirements.
    echo.
    pause
    exit /b
)

if not exist ".env" (
    echo.
    echo No .env found. Opening setup wizard...
    echo.
    %PYTHON_CMD% setup_wizard.py
)

echo.
echo Starting Gargamel's Bot...
echo.

%PYTHON_CMD% -u main.py

echo.
echo App stopped or crashed.
pause