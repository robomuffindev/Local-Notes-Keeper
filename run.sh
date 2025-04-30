#!/bin/bash
echo "======================================================="
echo "LocalNotes Application"
echo "======================================================="
echo

# Activate virtual environment
if [ -d "venv" ]; then
    source venv/bin/activate
elif [ -d "env" ]; then
    source env/bin/activate
else
    echo "Virtual environment not found. Please run setup first."
    exit 1
fi

echo "Starting LocalNotes server..."
echo
python app.py

# Deactivate virtual environment on exit
deactivate