# Script para iniciar el frontend (mobile)
# Uso: .\iniciar.ps1 [LOCAL|AZURE|PRODUCTION]

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("LOCAL", "AZURE", "PRODUCTION")]
    [string]$Entorno
)

# Si se especifica entorno como parámetro, cambiar antes de iniciar
if ($Entorno) {
    Write-Host "🔄 Configurando entorno: $Entorno" -ForegroundColor Yellow
    $env:ENVIRONMENT = $Entorno
}

# Leer entorno actual (prioridad: param > env > archivo estado > default)
if (-not $env:ENVIRONMENT) {
    if (Test-Path "$PSScriptRoot\.env_state") {
        $env:ENVIRONMENT = Get-Content "$PSScriptRoot\.env_state" -Raw
    } else {
        $env:ENVIRONMENT = "AZURE"
    }
}

# Mostrar información
Clear-Host
Write-Host "=== WhatsApp Manager ===" -ForegroundColor Cyan
Write-Host ""

# Mostrar entorno activo con color
$envColor = switch ($env:ENVIRONMENT) {
    "LOCAL" { "Green" }
    "AZURE" { "Blue" }
    "PRODUCTION" { "Magenta" }
    default { "White" }
}

Write-Host "[Entorno]  " -NoNewline -ForegroundColor Gray
Write-Host $env:ENVIRONMENT -ForegroundColor $envColor

if ($env:ENVIRONMENT -eq "LOCAL") {
    Write-Host "[Backend]  http://localhost:5000 (debes iniciarlo manualmente)" -ForegroundColor Yellow
    Write-Host ""
    Write-Host "[Tip] Inicia el backend en otra terminal con:" -ForegroundColor Gray
    Write-Host "      cd backend" -ForegroundColor Gray  
    Write-Host "      python back.py" -ForegroundColor Gray
} else {
    Write-Host "[Backend]  Azure App Services (ya corriendo 24/7)" -ForegroundColor Green
    Write-Host "           https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net" -ForegroundColor Gray
}

Write-Host ""
Write-Host "[Frontend] Iniciando aplicación local..." -ForegroundColor Yellow
Write-Host ""
Write-Host "[Tip] Cambia de entorno con: .\cambiar_entorno.ps1" -ForegroundColor Gray
Write-Host ""

Get-Process python* -ErrorAction SilentlyContinue | Where-Object {$_.Path -like "*CLAUDE-1*"} | Stop-Process -Force

# Iniciar frontend
& python C:\VS\CLAUDE-1\mobile\main.py
