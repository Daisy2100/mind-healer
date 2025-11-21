<#
.SYNOPSIS
    Universal Docker Build & Pack Script
.DESCRIPTION
    1. Check Docker environment
    2. Build Image (Force Tag)
    3. Export to tar file in 'dist' folder
#>

# ================= CONFIGURATION =================
$PROJECT_NAME = "Mind Healer Backend"   # Project Name
$IMAGE_NAME   = "mindhealer-backend"    # Docker Image Name
$IMAGE_TAG    = "latest"                # Tag Version
# =============================================

$ErrorActionPreference = "Stop"

function Log-Info ($Message) {
    Write-Host "[$((Get-Date).ToString('HH:mm:ss'))] $Message" -ForegroundColor Cyan
}

try {
    # 1. Check Docker Environment
    Log-Info "Checking Docker environment..."
    if (-not (Get-Command docker -ErrorAction SilentlyContinue)) { 
        throw "Docker CLI not found. Please install Docker Desktop." 
    }
    
    # FIX: Use 'docker version' instead of 'docker info' to avoid WSL2 kernel warnings
    # explicitly ignored output
    docker version | Out-Null
    
    if ($LASTEXITCODE -ne 0) { 
        throw "Docker Daemon is not running. Please start Docker Desktop." 
    }

    # 2. Build Image
    Log-Info "Building $PROJECT_NAME ($($IMAGE_NAME):$($IMAGE_TAG))..."
    
    docker build -t "$($IMAGE_NAME):$($IMAGE_TAG)" .
    
    if ($LASTEXITCODE -ne 0) { throw "Build failed." }

    # 3. Prepare Output Directory
    $distDir = Join-Path $PSScriptRoot "dist"
    if (-not (Test-Path $distDir)) { 
        New-Item -ItemType Directory -Path $distDir | Out-Null 
    }

    # 4. Export (Pack)
    $exportFile = "$distDir\$($IMAGE_NAME)-$(Get-Date -Format yyyyMMddHHmm).tar"
    Log-Info "Packaging image to: $exportFile"

    docker save -o $exportFile "$($IMAGE_NAME):$($IMAGE_TAG)"

    if ($LASTEXITCODE -eq 0) {
        Write-Host "`n[SUCCESS] File created:" -ForegroundColor Green
        Write-Host "   $exportFile" -ForegroundColor Gray
    } else {
        throw "Packaging failed."
    }

} catch {
    Write-Host "`n[ERROR]: $_" -ForegroundColor Red
    exit 1
}