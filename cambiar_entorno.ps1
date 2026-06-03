# Script para cambiar entre entorno LOCAL y AZURE con menú interactivo

param(
    [Parameter(Mandatory=$false)]
    [ValidateSet("LOCAL", "AZURE", "PRODUCTION")]
    [string]$Entorno
)

function Mostrar-Menu {
    Clear-Host
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host "    SELECTOR DE ENTORNO - WhatsApp     " -ForegroundColor Cyan
    Write-Host "========================================" -ForegroundColor Cyan
    Write-Host ""

    # Mostrar entorno actual
    $actualEnv = $env:ENVIRONMENT
    if (-not $actualEnv) { $actualEnv = "LOCAL" }
    Write-Host "Entorno actual: " -NoNewline
    Write-Host "$actualEnv" -ForegroundColor Yellow
    Write-Host ""

    Write-Host "Selecciona el entorno:" -ForegroundColor White
    Write-Host ""
    Write-Host "  [1] LOCAL" -ForegroundColor Green
    Write-Host "      http://localhost:5000" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  [2] AZURE" -ForegroundColor Blue
    Write-Host "      https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  [3] PRODUCTION" -ForegroundColor Magenta
    Write-Host "      (Requiere PRODUCTION_URL en variables de entorno)" -ForegroundColor Gray
    Write-Host ""
    Write-Host "  [0] Salir" -ForegroundColor Red
    Write-Host ""
    Write-Host "========================================" -ForegroundColor Cyan
}

if (-not $Entorno) {
    Mostrar-Menu
    $opcion = Read-Host "Opción"

    switch ($opcion) {
        "1" { $Entorno = "LOCAL" }
        "2" { $Entorno = "AZURE" }
        "3" { $Entorno = "PRODUCTION" }
        "0" {
            Write-Host "Cancelado" -ForegroundColor Yellow
            exit 0
        }
        default {
            Write-Host "Opción inválida" -ForegroundColor Red
            exit 1
        }
    }
}

Write-Host ""
Write-Host "[*] Cambiando entorno a: $Entorno" -ForegroundColor Cyan

# Establecer variable de entorno del sistema (persiste entre sesiones)
[System.Environment]::SetEnvironmentVariable("ENVIRONMENT", $Entorno, [System.EnvironmentVariableTarget]::User)

# Establecer para la sesión actual
$env:ENVIRONMENT = $Entorno

# Guardar en archivo de estado para referencia rápida
$Entorno | Out-File -FilePath "$PSScriptRoot\.env_state" -Encoding UTF8 -NoNewline

Write-Host "[OK] Entorno configurado: $Entorno" -ForegroundColor Green
Write-Host ""
Write-Host "[AVISO] Reinicia la aplicación para aplicar los cambios" -ForegroundColor Yellow
Write-Host "   Ejecuta: .\iniciar.ps1" -ForegroundColor Gray
