@echo off
where pythonw >nul 2>&1
if errorlevel 1 (
    echo Python 3 with pythonw is required to open the map.
    pause
    exit /b 1
)
start "" pythonw "%~dp0open_3d_map.py" zootlocker --background
