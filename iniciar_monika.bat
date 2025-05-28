@echo off
title Iniciando Monika Backend + NGROK

echo Iniciando servidor Flask...
start cmd /k "cd /d %~dp0 && python app.py"

timeout /t 2 >nul

echo Iniciando NGROK...
start cmd /k "cd /d %~dp0 && ngrok http 5000"

echo Tudo pronto! Lembre-se de copiar a URL HTTPS do NGROK pro GPT Builder.
pause
