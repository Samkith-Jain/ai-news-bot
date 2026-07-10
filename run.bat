@echo off
SETLOCAL Enabledelayedexpansion
title AI News Bot Orchestrator

echo ===================================================
echo             AI NEWS BOT ORCHESTRATOR           
echo ===================================================

:: 1. Check if Ollama is running locally on port 11434
echo [1/4] Checking Ollama local server status...
curl -s http://localhost:11434 >nul
if %errorlevel% neq 0 (
    echo [!] Ollama local engine is not active. Attempting to start...
    :: Launch Ollama in the background
    start "" "ollama" serve
    echo [^>] Ollama initialization signal sent. Waiting 5 seconds to bind...
    timeout /t 5 /nobreak >nul
) else (
    echo [^>] Ollama local engine is already running.
)

:: 2. Verify virtual environment exists
echo [2/4] Verifying local Python virtual environment...
if not exist "venv\Scripts\activate.bat" (
    echo [X] Error: Virtual environment 'venv' not found.
    echo Please run 'python -m venv venv' and install requirements first.
    pause
    exit /b
)

:: 3. Launch the Background News Scheduler in a separate background window
echo [3/4] Spawning background news scheduler (every 30 mins)...
start "AI News Bot - Scheduler" cmd /k "call venv\Scripts\activate.bat && python news_scheduler.py"

:: 4. Launch the Streamlit Frontend in the current terminal context
echo [4/4] Starting local Streamlit UI dashboard...
echo ===================================================
echo [SUCCESS] App launching! Keep this window open to maintain the UI.
echo ===================================================
call venv\Scripts\activate.bat
streamlit run app.py

pause