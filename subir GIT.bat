@echo off
cd /d C:\Users\migas\monika-backend

echo Inicializando Git...
git init

echo Adicionando arquivos...
git add .

echo Fazendo commit inicial...
git commit -m "Primeiro commit do projeto Monika Pokémon"

set /p repo_url=Digite a URL do repositório GitHub (ex: https://github.com/seunome/monika-backend.git): 

echo Conectando ao repositório remoto...
git remote add origin %repo_url%

echo Subindo código pro branch main...
git branch -M main
git push -u origin main

pause
