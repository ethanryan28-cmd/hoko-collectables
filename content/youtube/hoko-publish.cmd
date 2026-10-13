@echo off
rem Daily "HOKO publish" task — runs from the repo root, appends to content\youtube\publish.log
cd /d "%~dp0\..\.."
python content\youtube\run.py publish >> content\youtube\publish.log 2>&1
