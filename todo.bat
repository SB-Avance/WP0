Rem cd C:\VS\CLAUDE-1\backend
Rem python app.py
Rem cd C:\VS\CLAUDE-1\mobile
Rem python main.py

@echo off
echo Iniciando WhatsApp Manager...
start cmd /k "cd C:\VS\CLAUDE-1\backend && python app.py"
timeout /t 2
start cmd /k "cd C:\VS\CLAUDE-1\mobile && python main.py"