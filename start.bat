@echo off
echo Starting Gambler's Ruin Application...
echo.

rem Change to script directory
cd /d %~dp0

rem Check if virtual environment exists
if not exist venv\Scripts\activate.bat (
    echo Creating virtual environment...
    python -m venv venv
)

rem Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat

rem Install requirements
echo Installing requirements...
pip install -r requirements.txt

rem Define ports
set API_PORT=5000
set WEB_PORT=5050

echo.
echo Starting API server on port %API_PORT%...
start "Gambler's Ruin API Server" cmd /k "cd /d %~dp0 && call venv\Scripts\activate.bat && python -m src.api.app"

rem Wait for API server to start
timeout /t 2 /nobreak > nul

echo Starting web server on port %WEB_PORT%...
start "Gambler's Ruin Web Server" cmd /k "cd /d %~dp0 && call venv\Scripts\activate.bat && python -m web.serve"

rem Wait for web server to start
timeout /t 2 /nobreak > nul

echo Opening web browser...
start http://localhost:%WEB_PORT%

echo.
echo Application started successfully!
echo API Server running in separate window (port %API_PORT%)
echo Web Server running in separate window (port %WEB_PORT%)
echo Keep these windows open while using the application.
echo To stop the application, close both server windows.
echo.

pause 