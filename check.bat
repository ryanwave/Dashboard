@echo off
REM Checks that every document under C:\Dashboard can be opened and prints a report.
cd /d "%~dp0"
python run.py --root "C:\Dashboard" --check > dochub-check.txt 2>&1
type dochub-check.txt
echo.
echo Report saved to dochub-check.txt
pause
