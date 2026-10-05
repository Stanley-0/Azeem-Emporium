@echo off
setlocal
cd /d "%~dp0"

set "AZEEM_PYTHON=%CD%\.venv\Scripts\python.exe"

if not exist "%AZEEM_PYTHON%" (
  echo The local Python environment was not found.
  echo Expected: %AZEEM_PYTHON%
  pause
  exit /b 1
)

echo Starting Azeem Emporium locally...
start "Azeem Emporium Website" /b "%AZEEM_PYTHON%" "chatbot\api.py"
timeout /t 2 /nobreak >nul
start "" "http://127.0.0.1:5000"

echo The website is open at http://127.0.0.1:5000
echo Close this window to stop the local server.
pause >nul
