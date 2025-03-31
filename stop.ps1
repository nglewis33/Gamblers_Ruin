# PowerShell script to stop the Gambler's Ruin application
Write-Host "Stopping Gambler's Ruin Application..." -ForegroundColor Cyan

# Kill processes by window title
Write-Host "Stopping API server..." -ForegroundColor Yellow
Get-Process | Where-Object { $_.MainWindowTitle -like "*Gambler's Ruin API Server*" } | ForEach-Object { 
    $_ | Stop-Process -Force
}

Write-Host "Stopping web server..." -ForegroundColor Yellow
Get-Process | Where-Object { $_.MainWindowTitle -like "*Gambler's Ruin Web Server*" } | ForEach-Object { 
    $_ | Stop-Process -Force 
}

# For extra safety, check for Python processes listening on our ports
Write-Host "Checking for processes on ports 5000 and 5050..." -ForegroundColor Yellow
$processes5000 = Get-NetTCPConnection -LocalPort 5000 -State Listen -ErrorAction SilentlyContinue | 
                 ForEach-Object { Get-Process -Id $_.OwningProcess }
$processes5050 = Get-NetTCPConnection -LocalPort 5050 -State Listen -ErrorAction SilentlyContinue | 
                 ForEach-Object { Get-Process -Id $_.OwningProcess }

# Kill any Python processes found on those ports
if ($processes5000) {
    $processes5000 | Where-Object { $_.Name -eq "python" } | ForEach-Object {
        Write-Host "Stopping Python process on port 5000 (PID: $($_.Id))..." -ForegroundColor Yellow
        $_ | Stop-Process -Force
    }
}

if ($processes5050) {
    $processes5050 | Where-Object { $_.Name -eq "python" } | ForEach-Object {
        Write-Host "Stopping Python process on port 5050 (PID: $($_.Id))..." -ForegroundColor Yellow
        $_ | Stop-Process -Force
    }
}

Write-Host "Application stopped successfully!" -ForegroundColor Green

# Wait for user to press a key
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey('NoEcho,IncludeKeyDown') 