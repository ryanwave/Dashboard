@echo off
REM Starts DocHub on http://localhost:8080 serving C:\Dashboard
cd /d "%~dp0"
python run.py --root "C:\Dashboard" --port 8080
pause
