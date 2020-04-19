@echo off
TITLE Group Bot
rem This next line removes any fban csv files if they exist in root when bot restarts.
del *.csv
python -m tg_bot

pause
