@echo off
REM Builds a demo folder with sample documents + history, then starts DocHub on it.
cd /d "%~dp0"
python scripts\make_sample.py sample_data\Dashboard --seed-history
python run.py --root sample_data\Dashboard --port 8080
pause
