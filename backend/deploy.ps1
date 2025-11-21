# Mind Healer Backend - Docker Deployment Script for Windows

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Mind Healer Backend Deployment" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Check Docker installation (CLI)
$dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
if (-not $dockerInstalled) {
    Write-Host "Error: Docker CLI is not installed." -ForegroundColor Red
    Write-Host "Download: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
    exit 1
}

# Check Docker daemon is running
try {
    docker info > $null 2>&1
    if ($LASTEXITCODE -ne 0) { throw "docker daemon not responding" }
} catch {
    Write-Host "Error: Docker daemon is not running or not accessible." -ForegroundColor Red
    Write-Host "Start Docker Desktop or the Docker service and retry." -ForegroundColor Yellow
    exit 1
}

# Check .env file (optional — environment variables can be injected by GCP)
if (-not (Test-Path ".env")) {
    Write-Host "Warning: .env file not found. Proceeding — remember to inject API keys via environment variables in production." -ForegroundColor Yellow
}

# Check books directory
if (-not (Test-Path "books")) {
    Write-Host "Warning: books directory not found" -ForegroundColor Yellow
    Write-Host "Creating books directory..." -ForegroundColor Yellow
    New-Item -ItemType Directory -Path "books" | Out-Null
    Write-Host "Please add .txt files to the books directory" -ForegroundColor Yellow
}

# Build image only (no start/run)
Write-Host "Building Docker image (pack only)..." -ForegroundColor Yellow
docker-compose build
if ($LASTEXITCODE -ne 0) {
    Write-Host "Docker build failed (exit code $LASTEXITCODE). Check output above." -ForegroundColor Red
    exit 1
}

# Export image to tar (packaging step)
# Change this to the image you want to save (e.g., couchdb12 or mindhealer-backend)
$exportImage = "mindhealer-backend"
$distDir = Join-Path $PSScriptRoot "dist"
if (-not (Test-Path $distDir)) { New-Item -ItemType Directory -Path $distDir | Out-Null }
$exportFile = "$distDir\$($exportImage)-$(Get-Date -Format yyyyMMddHHmm).tar"

Write-Host "`nPackaging image '$exportImage' to: $exportFile" -ForegroundColor Cyan
if (docker image inspect $exportImage > $null 2>&1) {
    try {
        Write-Host "Running: docker save $exportImage > $exportFile" -ForegroundColor DarkCyan
        docker save $exportImage > $exportFile
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Export succeeded: $exportFile" -ForegroundColor Green
        } else {
            Write-Host "Export failed with exit code $LASTEXITCODE" -ForegroundColor Red
            exit 1
        }
    } catch {
        Write-Host "docker save failed: $_" -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "Image '$exportImage' not found locally. Attempting to auto-detect built image..." -ForegroundColor Yellow
    $images = docker images --format "{{.Repository}}:{{.Tag}} {{.ID}}" 2>$null
    $candidate = $null
    foreach ($line in $images) {
        if ($line -match "^mindhealer-backend:|mindhealer-backend ") {
            $parts = $line -split ' '
            $candidate = $parts[0]
            break
        }
    }
    if (-not $candidate) {
        # fallback: try any image repo containing 'backend' and tag 'latest'
        foreach ($line in $images) {
            if ($line -match "backend.*:latest") {
                $parts = $line -split ' '
                $candidate = $parts[0]
                break
            }
        }
    }
    if ($candidate) {
        Write-Host "Detected image to export: $candidate" -ForegroundColor Cyan
        Write-Host "Running: docker save $candidate > $exportFile" -ForegroundColor DarkCyan
        docker save $candidate > $exportFile
        if ($LASTEXITCODE -eq 0) {
            Write-Host "Export succeeded: $exportFile" -ForegroundColor Green
        } else {
            Write-Host "Export failed with exit code $LASTEXITCODE" -ForegroundColor Red
            exit 1
        }
    } else {
        Write-Host "Could not auto-detect an image to export." -ForegroundColor Red
        Write-Host "Available images:" -ForegroundColor Yellow
        docker images --format "{{.Repository}}:{{.Tag}}\t{{.ID}}" | Select-Object -First 50
        exit 1
    }
}
