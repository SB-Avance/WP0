Write-Host "Iniciando WhatsApp Manager desde PowerShell..." -ForegroundColor Green

# Verificar entorno configurado
$entorno = [System.Environment]::GetEnvironmentVariable("ENVIRONMENT", [System.EnvironmentVariableTarget]::User)
if ([string]::IsNullOrEmpty($entorno)) {
    $entorno = "AZURE"  # Por defecto AZURE (backend en la nube)
}

Write-Host "Entorno configurado: $entorno" -ForegroundColor Cyan

if ($entorno -eq "AZURE") {
    Write-Host "Conectando a Azure App Services" -ForegroundColor Yellow
    Write-Host "URL: https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net" -ForegroundColor Gray
} else {
    Write-Host "Conectando a backend LOCAL" -ForegroundColor Yellow
    Write-Host "URL: http://localhost:5000" -ForegroundColor Gray
}

Write-Host ""

# Iniciar la App Movil con la variable de entorno
$comando = "cd C:\VS\CLAUDE-1\mobile; `$env:ENVIRONMENT='$entorno'; python main.py"
Start-Process powershell -ArgumentList "-NoExit", "-Command", $comando

Write-Host "[OK] App movil iniciada" -ForegroundColor Green
