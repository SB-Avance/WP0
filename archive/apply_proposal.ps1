param(
    [switch]$Apply
)

# Script seguro para mover los archivos listados en `archive/PROPOSED_MOVE_LIST.md` a
# `archive/YYYYMMDD_HHMMSS/`. Por defecto corre en modo simulación (WhatIf).

$proposal = Join-Path $PSScriptRoot 'PROPOSED_MOVE_LIST.md'
if (-not (Test-Path $proposal)) { Write-Error "No se encontró $proposal"; exit 2 }

$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$destRoot = Join-Path $PSScriptRoot $timestamp

Write-Output "Leyendo propuesta: $proposal"
$lines = Get-Content $proposal | Where-Object { $_ -and $_ -notmatch '^(#|\+|-\s*$)' }

$items = @()
foreach ($l in $lines) {
    $trim = $l.TrimStart('+- ').Trim()
    if ($trim) { $items += $trim }
}

if (-not $items) { Write-Output 'No hay items detectados en la propuesta.'; exit 0 }

Write-Output "Se detectaron $($items.Count) items. Destino: $destRoot"

foreach ($it in $items) {
    $src = Join-Path (Resolve-Path "$PSScriptRoot\.." | Select-Object -First 1) $it
    $rel = $it -replace '[\\/]','/'
    $dest = Join-Path $destRoot $rel
    $destDir = Split-Path $dest -Parent
    if (-not (Test-Path $src)) { Write-Warning "No existe: $src -- se omite."; continue }
    if (-not (Test-Path $destDir)) { New-Item -ItemType Directory -Path $destDir -Force | Out-Null }
    if ($Apply) {
        Move-Item -Path $src -Destination $dest -Force
        Write-Output "Movido: $src -> $dest"
    } else {
        Write-Output "(Simulation) Mover: $src -> $dest"
    }
}

if (-not $Apply) {
    Write-Output 'Ejecución en modo simulación. Para aplicar realmente, ejecuta: .\apply_proposal.ps1 -Apply desde la carpeta archive/'
} else {
    Write-Output ("Movimientos realizados. Revisa la carpeta: {0}" -f $destRoot)
}
