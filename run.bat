@echo off
echo =======================================================
echo LocalNotes Application
echo =======================================================
echo.
call venv\Scripts\activate.bat
echo Starting LocalNotes server...
echo.
python app.py
if %errorlevel% neq 0 (
    echo Failed to start the application.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)