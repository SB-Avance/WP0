Write-Host "Iniciando WhatsApp Manager desde PowerShell..." -ForegroundColor Green

# 1. Iniciar el Backend en una nueva ventana de PowerShell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\VS\CLAUDE-1\backend; python app.py"

# 2. Tiempo de espera (2 segundos)
Start-Sleep -Seconds 2

# 3. Iniciar la App Móvil (Flet/Python) en otra ventana de PowerShell
Start-Process powershell -ArgumentList "-NoExit", "-Command", "cd C:\VS\CLAUDE-1\mobile; python main.py"

Write-Host "Procesos lanzados con éxito." -ForegroundColor Green
