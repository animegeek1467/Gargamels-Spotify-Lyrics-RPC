@echo off
cd /d "%~dp0"

title Install Gargamel's Bot Requirements

where py >nul 2>nul
if %ERRORLEVEL%==0 (
    set "PYTHON_CMD=py -3"
) else (
    set "PYTHON_CMD=python"
)

echo Installing requirements...
%PYTHON_CMD% -m pip install -r requirements.txt

echo.
echo Done.
pause