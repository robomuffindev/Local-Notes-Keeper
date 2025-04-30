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
pip install flask flask-wtf werkzeug
if %errorlevel% neq 0 (
    echo Failed to install dependencies.
    echo Press any key to exit...
    pause > nul
    exit /b 1
)

REM Create necessary directories
echo Creating application structure...
if not exist app_data mkdir app_data
if not exist static mkdir static
if not exist static\css mkdir static\css
if not exist static\js mkdir static\js
if not exist templates mkdir templates

REM Create the Jinja2 custom filters
echo Creating Jinja2 filters...
echo from datetime import datetime > filters.py
echo. >> filters.py
echo def format_datetime(value): >> filters.py
echo     if not value: >> filters.py
echo         return "" >> filters.py
echo     dt = datetime.fromisoformat(value) >> filters.py
echo     return dt.strftime('%%Y-%%m-%%d %%H:%%M') >> filters.py
echo. >> filters.py
echo def format_size(bytes): >> filters.py
echo     if bytes == 0: >> filters.py
echo         return "0B" >> filters.py
echo     size_names = ["B", "KB", "MB", "GB", "TB"] >> filters.py
echo     i = 0 >> filters.py
echo     while bytes >= 1024 and i < len(size_names)-1: >> filters.py
echo         bytes /= 1024 >> filters.py
echo         i += 1 >> filters.py
echo     return f"{bytes:.1f}{size_names[i]}" >> filters.py
echo. >> filters.py
echo def nl2br(value): >> filters.py
echo     return value.replace('\n', '<br>') if value else '' >> filters.py

REM Update app.py to use filters
echo from flask import Flask, render_template >> app_temp.py
echo from filters import format_datetime, format_size, nl2br >> app_temp.py
echo. >> app_temp.py
echo app = Flask(__name__) >> app_temp.py
echo app.jinja_env.filters['format_datetime'] = format_datetime >> app_temp.py
echo app.jinja_env.filters['format_size'] = format_size >> app_temp.py
echo app.jinja_env.filters['nl2br'] = nl2br >> app_temp.py
echo # Rest of app.py contents will be copied here >> app_temp.py

REM Create run.bat
echo @echo off > run.bat
echo echo ======================================================= >> run.bat
echo echo LocalNotes Application >> run.bat
echo echo ======================================================= >> run.bat
echo echo. >> run.bat
echo call venv\Scripts\activate.bat >> run.bat
echo echo Starting LocalNotes server... >> run.bat
echo echo. >> run.bat
echo python app.py >> run.bat
echo if %%errorlevel%% neq 0 ( >> run.bat
echo     echo Failed to start the application. >> run.bat
echo     echo Press any key to exit... >> run.bat
echo     pause ^> nul >> run.bat
echo     exit /b 1 >> run.bat
echo ) >> run.bat

echo.
echo Installation completed successfully!
echo You can now run the application using run.bat
echo.
echo Press any key to exit...
pause > nul

exit /b 0