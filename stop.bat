@echo off
echo Stopping Gambler's Ruin Application...

rem Kill all running Python instances with specific window titles
echo Stopping API server...
taskkill /FI "WINDOWTITLE eq Gambler's Ruin API Server*" /T /F > nul 2>&1

echo Stopping web server...
taskkill /FI "WINDOWTITLE eq Gambler's Ruin Web Server*" /T /F > nul 2>&1

echo.
echo Application stopped successfully!
echo.

pause 