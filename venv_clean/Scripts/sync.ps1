# Script para sincronizar cambios con GitHub automaticamente
# Uso: .\sync.ps1 "Mensaje del commit"

param(
    [Parameter(Mandatory=$false)]
    [string]$Mensaje = "Update: Cambios automaticos"
)

Write-Host "[*] Iniciando sincronizacion con GitHub..." -ForegroundColor Cyan
Write-Host ""

# 1. Verificar estado
Write-Host "[*] Verificando cambios..." -ForegroundColor Yellow
git status --short

$cambios = git status --porcelain
if ([string]::IsNullOrWhiteSpace($cambios)) {
    Write-Host "[OK] No hay cambios para sincronizar" -ForegroundColor Green
    exit 0
}

Write-Host ""

# 2. Agregar todos los cambios
Write-Host "[+] Agregando archivos al stage..." -ForegroundColor Yellow
git add -A
Write-Host "[OK] Archivos agregados" -ForegroundColor Green
Write-Host ""

# 3. Hacer commit
Write-Host "[*] Haciendo commit con mensaje: '$Mensaje'" -ForegroundColor Yellow
git commit -m "$Mensaje"
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error al hacer commit" -ForegroundColor Red
    exit 1
}
Write-Host "[OK] Commit realizado" -ForegroundColor Green
Write-Host ""

# 4. Subir a GitHub
Write-Host "[*] Subiendo cambios a GitHub..." -ForegroundColor Yellow
git push origin main
if ($LASTEXITCODE -ne 0) {
    Write-Host "[ERROR] Error al hacer push" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "[OK] Sincronizacion completada exitosamente!" -ForegroundColor Green
Write-Host "[>] Revisa tus cambios en: https://github.com/SBApoyo/WP0" -ForegroundColor Cyan
