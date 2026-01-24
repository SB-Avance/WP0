# Script para iniciar SOLO el frontend (mobile)
# El backend YA esta corriendo en Azure App Services 24/7

Write-Host "=== WhatsApp Manager ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "[Backend]  Azure App Services (ya corriendo)" -ForegroundColor Green
Write-Host "           https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net" -ForegroundColor Gray
Write-Host ""
Write-Host "[Frontend] Iniciando aplicacion local..." -ForegroundColor Yellow
Write-Host ""

# Establecer entorno AZURE
$env:ENVIRONMENT = "AZURE"

# Iniciar frontend
cd C:\VS\CLAUDE-1\mobile
python main.py
