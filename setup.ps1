# Mind Healer Quick Setup Script
# This script will automatically download data, setup environment and start the project

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Mind Healer Quick Setup" -ForegroundColor Cyan
Write-Host "========================================`n" -ForegroundColor Cyan

# Step 1: Check and download data
Write-Host "Step 1/4: Checking data..." -ForegroundColor Yellow

if (Test-Path "books") {
    Write-Host "Books folder exists" -ForegroundColor Green
    $downloadBooks = Read-Host "Re-download data? (y/N)"
    if ($downloadBooks -eq "y" -or $downloadBooks -eq "Y") {
        Remove-Item "books" -Recurse -Force
        $needDownload = $true
    } else {
        $needDownload = $false
    }
} else {
    $needDownload = $true
}

if ($needDownload) {
    Write-Host "Downloading books.zip..." -ForegroundColor Yellow
    try {
        Invoke-WebRequest -Uri "https://github.com/yenlung/AI-Demo/raw/refs/heads/master/books.zip" -OutFile "books.zip"
        Write-Host "Extracting..." -ForegroundColor Yellow
        Expand-Archive -Path "books.zip" -DestinationPath "." -Force
        Remove-Item "books.zip"
        Write-Host "Data download completed" -ForegroundColor Green
    } catch {
        Write-Host "Download failed: $_" -ForegroundColor Red
        Write-Host "Please manually download and extract books.zip" -ForegroundColor Yellow
    }
}

# Step 2: Setup LLM
Write-Host "`nStep 2/4: Setting up LLM..." -ForegroundColor Yellow

if (Test-Path "backend\.env") {
    Write-Host ".env file exists" -ForegroundColor Green
    $recreateEnv = Read-Host "Recreate .env? (y/N)"
    if ($recreateEnv -eq "y" -or $recreateEnv -eq "Y") {
        $needSetupEnv = $true
    } else {
        $needSetupEnv = $false
    }
} else {
    $needSetupEnv = $true
}

if ($needSetupEnv) {
    Write-Host "`nChoose LLM Provider:" -ForegroundColor Cyan
    Write-Host "1. Google Gemini (Recommended - Largest free quota)" -ForegroundColor Green
    Write-Host "2. Groq (Free and super fast)" -ForegroundColor Green
    Write-Host "3. Ollama (Local, completely free)" -ForegroundColor Green
    Write-Host "4. OpenAI (Paid, best quality)" -ForegroundColor Yellow
    Write-Host "5. Skip, setup manually later" -ForegroundColor White
    
    $llmChoice = Read-Host "Choose (1-5)"
    
    Copy-Item "backend\.env.example" -Destination "backend\.env" -Force
    
    switch ($llmChoice) {
        "1" {
            Write-Host "`nEnter your Google API Key (AIza...):" -ForegroundColor Yellow
            Write-Host "Sign up: https://makersuite.google.com/app/apikey" -ForegroundColor Cyan
            Write-Host "Or visit: https://aistudio.google.com/app/apikey" -ForegroundColor Cyan
            $apiKey = Read-Host
            
            if ($apiKey -match "^AIza") {
                $envContent = "GOOGLE_API_KEY=$apiKey"
                Set-Content -Path "backend\.env" -Value $envContent
                Write-Host "Google Gemini API Key configured" -ForegroundColor Green
                Write-Host "Note: Install package: pip install langchain-google-genai" -ForegroundColor Yellow
            } else {
                Write-Host "API Key format seems incorrect" -ForegroundColor Yellow
            }
        }
        "2" {
            Write-Host "`nEnter your Groq API Key (gsk_...):" -ForegroundColor Yellow
            Write-Host "Sign up: https://console.groq.com/keys" -ForegroundColor Cyan
            $apiKey = Read-Host
            
            if ($apiKey -match "^gsk_") {
                $envContent = "GROQ_API_KEY=$apiKey"
                Set-Content -Path "backend\.env" -Value $envContent
                Write-Host "Groq API Key configured" -ForegroundColor Green
                Write-Host "Note: Install package: pip install langchain-groq" -ForegroundColor Yellow
            } else {
                Write-Host "API Key format seems incorrect" -ForegroundColor Yellow
            }
        }
        "3" {
            Write-Host "`nOllama (local model) selected" -ForegroundColor Green
            Write-Host "Please ensure:" -ForegroundColor Yellow
            Write-Host "1. Ollama is installed: https://ollama.ai" -ForegroundColor White
            Write-Host "2. Run: ollama pull llama3.1" -ForegroundColor White
            Write-Host "3. Ollama service is running" -ForegroundColor White
            Set-Content -Path "backend\.env" -Value "# Using Ollama (local model, no API Key needed)"
        }
        "4" {
            Write-Host "`nEnter your OpenAI API Key (sk-...):" -ForegroundColor Yellow
            $apiKey = Read-Host
            
            if ($apiKey -match "^sk-") {
                $envContent = "OPENAI_API_KEY=$apiKey"
                Set-Content -Path "backend\.env" -Value $envContent
                Write-Host "OpenAI API Key configured" -ForegroundColor Green
            } else {
                Write-Host "API Key format seems incorrect" -ForegroundColor Yellow
            }
        }
        "5" {
            Write-Host "Please manually edit backend\.env later" -ForegroundColor Yellow
        }
        default {
            Write-Host "Invalid choice, please manually edit backend\.env" -ForegroundColor Yellow
        }
    }
}

# Step 3: Choose startup method
Write-Host "`nStep 3/4: Choose startup method..." -ForegroundColor Yellow
Write-Host "1. Use Docker (Recommended)" -ForegroundColor White
Write-Host "2. Local development mode" -ForegroundColor White
Write-Host "3. Setup only, start manually later" -ForegroundColor White

$choice = Read-Host "Choose (1-3)"

switch ($choice) {
    "1" {
        Write-Host "`nStarting with Docker..." -ForegroundColor Yellow
        
        # Check if Docker is installed
        $dockerInstalled = Get-Command docker -ErrorAction SilentlyContinue
        if (-not $dockerInstalled) {
            Write-Host "Docker not detected, please install Docker Desktop first" -ForegroundColor Red
            Write-Host "Download: https://www.docker.com/products/docker-desktop" -ForegroundColor Yellow
            exit
        }
        
        Write-Host "Starting Docker containers..." -ForegroundColor Yellow
        docker-compose up --build
    }
    "2" {
        Write-Host "`nLocal development mode..." -ForegroundColor Yellow
        Write-Host "Please run in two terminals:" -ForegroundColor Yellow
        Write-Host "`nTerminal 1 (Backend):" -ForegroundColor Cyan
        Write-Host "  cd backend" -ForegroundColor White
        Write-Host "  python -m venv venv" -ForegroundColor White
        Write-Host "  .\venv\Scripts\Activate.ps1" -ForegroundColor White
        Write-Host "  pip install -r requirements.txt" -ForegroundColor White
        Write-Host "  python main.py" -ForegroundColor White
        Write-Host "`nTerminal 2 (Frontend):" -ForegroundColor Cyan
        Write-Host "  cd frontend" -ForegroundColor White
        Write-Host "  npm install" -ForegroundColor White
        Write-Host "  npm run dev" -ForegroundColor White
    }
    "3" {
        Write-Host "`nSetup completed!" -ForegroundColor Green
    }
    default {
        Write-Host "`nInvalid choice" -ForegroundColor Red
    }
}

# Step 4: Display summary
Write-Host "`n========================================" -ForegroundColor Cyan
Write-Host "Setup Summary" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan

if (Test-Path "books") {
    $txtFiles = (Get-ChildItem "books\*.txt" -ErrorAction SilentlyContinue).Count
    Write-Host "Data: $txtFiles .txt files" -ForegroundColor Green
} else {
    Write-Host "Data: books folder not found" -ForegroundColor Red
}

if (Test-Path "backend\.env") {
    Write-Host "API Key: Configured" -ForegroundColor Green
} else {
    Write-Host "API Key: Not configured" -ForegroundColor Red
}

Write-Host "`nAccess URLs:" -ForegroundColor Cyan
Write-Host "  Frontend: http://localhost (Docker) or http://localhost:5173 (Local)" -ForegroundColor White
Write-Host "  Backend: http://localhost:8000" -ForegroundColor White
Write-Host "  API Docs: http://localhost:8000/docs" -ForegroundColor White

Write-Host "`nMore Information:" -ForegroundColor Cyan
Write-Host "  Quick Start: QUICKSTART.md" -ForegroundColor White
Write-Host "  Data Setup: DATA_SETUP.md" -ForegroundColor White
Write-Host "  Project Info: README.md" -ForegroundColor White

Write-Host "`nSetup completed! Enjoy!" -ForegroundColor Green
