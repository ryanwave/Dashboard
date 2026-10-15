@echo off
REM One-time setup: installs the Python packages DocHub needs.
cd /d "%~dp0"
python -m pip install --upgrade -r requirements.txt
pause
