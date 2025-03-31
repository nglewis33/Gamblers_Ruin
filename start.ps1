# PowerShell script to start the Gambler's Ruin application
Write-Host "Starting Gambler's Ruin Application..." -ForegroundColor Cyan

# Define script directory path
$scriptPath = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptPath

# Check if virtual environment exists
if (-not (Test-Path ".\venv\Scripts\activate.ps1")) {
    Write-Host "Creating virtual environment..." -ForegroundColor Yellow
    python -m venv venv
}

# Activate virtual environment
Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& .\venv\Scripts\activate.ps1

# Install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
pip install -r requirements.txt

# Define API server port and web server port
$apiPort = 5000
$webPort = 5050

# Check if API port is already in use
$apiPortInUse = Get-NetTCPConnection | Where-Object { $_.LocalPort -eq $apiPort -and $_.State -eq "Listen" } -ErrorAction SilentlyContinue
if ($apiPortInUse) {
    Write-Host "Warning: Port $apiPort is already in use. The API server might not start correctly." -ForegroundColor Red
}

# Check if web port is already in use
$webPortInUse = Get-NetTCPConnection | Where-Object { $_.LocalPort -eq $webPort -and $_.State -eq "Listen" } -ErrorAction SilentlyContinue
if ($webPortInUse) {
    Write-Host "Warning: Port $webPort is already in use. The web server might not start correctly." -ForegroundColor Red
}

# Start API server in a new window
Write-Host "Starting API server on port $apiPort..." -ForegroundColor Green
$apiServerProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {Set-Location '$scriptPath'; & .\venv\Scripts\activate.ps1; python -m src.api.app}" -PassThru

# Wait a bit to make sure API server starts
Start-Sleep -Seconds 2

# Start web server in a new window
Write-Host "Starting web server on port $webPort..." -ForegroundColor Green
$webServerProcess = Start-Process powershell -ArgumentList "-NoExit", "-Command", "& {Set-Location '$scriptPath'; & .\venv\Scripts\activate.ps1; python -m web.serve}" -PassThru

# Wait a bit to make sure web server starts
Start-Sleep -Seconds 2

# Open browser to the web interface
Write-Host "Opening web browser to http://localhost:$webPort..." -ForegroundColor Green
Start-Process "http://localhost:$webPort"

Write-Host "Application started successfully!" -ForegroundColor Cyan
Write-Host "API Server running in separate window (port $apiPort)"
Write-Host "Web Server running in separate window (port $webPort)"
Write-Host "Keep these windows open while using the application."
Write-Host "To stop the application, close both server windows." 