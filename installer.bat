@echo off
REM installer.bat - Install LocalNotes application and dependencies

echo ====================================
echo LocalNotes Installer
echo ====================================
echo.

REM Check if Python is installed
python --version > nul 2>&1
if %errorlevel% neq 0 (
    echo Python is not installed. Please install Python 3.8 or higher.
    echo You can download Python from https://www.python.org/downloads/
    echo.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

REM Create virtual environment
echo Creating virtual environment...
python -m venv venv
if %errorlevel% neq 0 (
    echo Failed to create virtual environment.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

REM Activate virtual environment and install dependencies
echo Installing dependencies...
call venv\Scripts\activate.bat
pip install flask werkzeug
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

REM Create app_data directory if it doesn't exist
if not exist app_data mkdir app_data

echo.
echo Installation completed successfully!
echo You can now run the application using run.bat
echo.
echo Press any key to exit...
pause > nul

exit /b 0