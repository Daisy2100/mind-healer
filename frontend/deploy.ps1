# Frontend Deployment Script for Mind Healer
Write-Host "Starting Mind Healer Frontend Deployment..." -ForegroundColor Green

# Build Docker image
Write-Host "`nBuilding Docker image..." -ForegroundColor Cyan
docker build -t mindhealer-frontend:latest .

if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed!" -ForegroundColor Red
    exit 1
}

Write-Host "`nDocker image built successfully!" -ForegroundColor Green

# Stop and remove old container if exists
Write-Host "`nStopping old container..." -ForegroundColor Cyan
docker stop mindhealer-frontend 2>$null
docker rm mindhealer-frontend 2>$null

# Run new container
Write-Host "`nStarting new container..." -ForegroundColor Cyan
docker run -d `
    --name mindhealer-frontend `
    --network mind-healer-network `
    -p 80:80 `
    --restart unless-stopped `
    mindhealer-frontend:latest

if ($LASTEXITCODE -ne 0) {
    Write-Host "Failed to start container!" -ForegroundColor Red
    exit 1
}

Write-Host "`n==================================" -ForegroundColor Green
Write-Host "Frontend Deployment Complete!" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Green
Write-Host "`nContainer Status:" -ForegroundColor Cyan
docker ps --filter name=mindhealer-frontend

Write-Host "`n🌐 Frontend is running at:" -ForegroundColor Yellow
Write-Host "   Local: http://localhost" -ForegroundColor White
Write-Host "   Production: https://mindhealer.daisy2100.com" -ForegroundColor White
