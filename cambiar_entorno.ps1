# Script para cambiar entre entorno LOCAL y AZURE

param(
    [Parameter(Mandatory=$true)]
    [ValidateSet("LOCAL", "AZURE", "PRODUCTION")]
    [string]$Entorno
)

Write-Host "🔄 Cambiando entorno a: $Entorno" -ForegroundColor Cyan

# Establecer variable de entorno del sistema
[System.Environment]::SetEnvironmentVariable("ENVIRONMENT", $Entorno, [System.EnvironmentVariableTarget]::User)

# Establecer para la sesión actual
$env:ENVIRONMENT = $Entorno

Write-Host "✅ Entorno configurado: $Entorno" -ForegroundColor Green
Write-Host ""
Write-Host "URLs configuradas:" -ForegroundColor Yellow
Write-Host "  LOCAL      -> http://localhost:5000" -ForegroundColor White
Write-Host "  AZURE      -> https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net" -ForegroundColor White
Write-Host "  PRODUCTION -> (configurar PRODUCTION_URL)" -ForegroundColor White
Write-Host ""
Write-Host "Para aplicar los cambios, reinicia la aplicación móvil." -ForegroundColor Cyan
