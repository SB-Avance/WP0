# Script rapido para sincronizar sin pedir mensaje
# Solo ejecuta: .\quick-sync.ps1

Write-Host "[*] Sincronizacion rapida..." -ForegroundColor Cyan

$fecha = Get-Date -Format "yyyy-MM-dd HH:mm"
$mensaje = "Update: Cambios del $fecha"

git add -A
git commit -m "$mensaje"
git push origin main

if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Listo! Cambios subidos a GitHub" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Error en la sincronizacion" -ForegroundColor Red
}
