@echo off
REM One-time setup: installs the Python packages DocHub needs.
cd /d "%~dp0"
python -m pip install -r requirements.txt
pause
