@echo off
title Trenddesen Kumaş & Desen Platformu
echo ========================================================
echo    Trenddesen Kumaş & Desen Kataloğu Başlatılıyor...
echo    trenddesen.com
echo ========================================================
echo.
cd /d "%~dp0"
python -m pip install -r requirements.txt
echo.
echo Tarayıcınızda açılıyor: http://127.0.0.1:8001
start http://127.0.0.1:8001
python -m uvicorn app:app --host 127.0.0.1 --port 8001 --reload
pause

