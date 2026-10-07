@echo off
rem Double-click to start the Tawazun demo. Close this window (or press Ctrl+C) to stop it.
rem Runs from this file's own folder, so .streamlit\config.toml (the deck theme) is picked up.
cd /d "%~dp0"

set "STREAMLIT=%USERPROFILE%\AppData\Local\Python\anaconda\envs\tawazun\Scripts\streamlit.exe"
if not exist "%STREAMLIT%" (
    echo Could not find Streamlit in the "tawazun" conda environment:
    echo   %STREAMLIT%
    echo Create it with: conda create -n tawazun python=3.12  then  pip install -r requirements.txt
    pause
    exit /b 1
)

"%STREAMLIT%" run app.py
pause
