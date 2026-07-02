$scriptPath = $PSScriptRoot

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "      Starting Flaskcard System          " -ForegroundColor Cyan
Write-Host "=========================================" -ForegroundColor Cyan

# 1. Start Backend
Write-Host "Starting Backend (FastAPI)..." -ForegroundColor Green
$backend = Start-Process "$scriptPath\.venv\Scripts\python.exe" -ArgumentList "-m", "uvicorn", "app.main:app", "--reload", "--port", "8000" -WorkingDirectory "$scriptPath\backend" -NoNewWindow -PassThru

# 2. Start Frontend
Write-Host "Starting Frontend (Vite/React)..." -ForegroundColor Yellow
$frontend = Start-Process "npm.cmd" -ArgumentList "run", "dev" -WorkingDirectory "$scriptPath\frontend" -NoNewWindow -PassThru

Write-Host "Done! Both Backend and Frontend are running in this terminal." -ForegroundColor White
Write-Host "Frontend will be available at http://localhost:5173" -ForegroundColor White
Write-Host "Backend API is running at http://localhost:8000" -ForegroundColor White
Write-Host "Press Ctrl+C to stop the services." -ForegroundColor Red

try {
    Wait-Process -Id $backend.Id, $frontend.Id
}
finally {
    if ($backend) { Stop-Process -Id $backend.Id -Force -ErrorAction SilentlyContinue }
    if ($frontend) { Stop-Process -Id $frontend.Id -Force -ErrorAction SilentlyContinue }
}
