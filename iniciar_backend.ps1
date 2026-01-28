# Script para iniciar el backend local
# Uso: .\iniciar_backend.ps1

Write-Host "=== Backend Local - WhatsApp Manager ===" -ForegroundColor Cyan
Write-Host ""
Write-Host "[*] Iniciando servidor Flask en modo LOCAL..." -ForegroundColor Yellow
Write-Host "[*] El servidor estará disponible en: http://localhost:5000" -ForegroundColor Green
Write-Host ""
Write-Host "[Tip] Para usar este backend, ejecuta en otra terminal:" -ForegroundColor Gray
Write-Host "      .\iniciar.ps1 LOCAL" -ForegroundColor Gray
Write-Host ""

# Establecer entorno LOCAL
$env:ENVIRONMENT = "LOCAL"

# Ir al directorio del backend
Set-Location "$PSScriptRoot\backend"

# Iniciar Flask
python back.py
