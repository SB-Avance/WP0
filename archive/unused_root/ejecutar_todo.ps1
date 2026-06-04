# Script PowerShell para Ejecutar Implementación Completa
# ========================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "IMPLEMENTACIÓN Y EJECUCIÓN COMPLETA DEL SISTEMA" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""

# Verificar que Python esté disponible
Write-Host "→ Verificando Python..." -ForegroundColor Yellow
$pythonVersion = python --version 2>&1
if ($LASTEXITCODE -eq 0) {
    Write-Host "  ✓ $pythonVersion" -ForegroundColor Green
} else {
    Write-Host "  ✗ Python no encontrado" -ForegroundColor Red
    exit 1
}

# Verificar archivos necesarios
Write-Host "`n→ Verificando archivos necesarios..." -ForegroundColor Yellow

$archivosRequeridos = @(
    "JSON_LISTO_PARA_INSERTAR.json",
    "sistema_menu_json.py",
    "implementar_todo.py",
    "demo_sistema_completo.py"
)

$archivosFaltantes = @()
foreach ($archivo in $archivosRequeridos) {
    if (Test-Path $archivo) {
        Write-Host "  ✓ $archivo" -ForegroundColor Green
    } else {
        Write-Host "  ✗ $archivo (faltante)" -ForegroundColor Red
        $archivosFaltantes += $archivo
    }
}

if ($archivosFaltantes.Count -gt 0) {
    Write-Host "`n✗ Faltan archivos necesarios. Abortando." -ForegroundColor Red
    exit 1
}

# Verificar variables de entorno
Write-Host "`n→ Verificando configuración..." -ForegroundColor Yellow

$configLista = $true

if ($env:DATAVERSE_URL) {
    Write-Host "  ✓ DATAVERSE_URL configurado" -ForegroundColor Green
} else {
    Write-Host "  ⚠ DATAVERSE_URL no configurado (requerido para Dataverse)" -ForegroundColor Yellow
    $configLista = $false
}

if ($env:CLIENT_ID) {
    Write-Host "  ✓ CLIENT_ID configurado" -ForegroundColor Green
} else {
    Write-Host "  ⚠ CLIENT_ID no configurado (requerido para Dataverse)" -ForegroundColor Yellow
    $configLista = $false
}

# Menú de opciones
Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "OPCIONES DE EJECUCIÓN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Demo Completa (sin Dataverse)" -ForegroundColor White
Write-Host "   → Simula el flujo completo del chatbot" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Modo Interactivo (sin Dataverse)" -ForegroundColor White
Write-Host "   → Prueba el sistema paso a paso" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Implementar en Dataverse y Ejecutar Demo" -ForegroundColor White
Write-Host "   → Inserta JSON y ejecuta demo (requiere credenciales)" -ForegroundColor Gray
Write-Host ""
Write-Host "4. Solo Implementar en Dataverse" -ForegroundColor White
Write-Host "   → Inserta JSON sin ejecutar demo" -ForegroundColor Gray
Write-Host ""

$opcion = Read-Host "Selecciona una opción (1-4)"

switch ($opcion) {
    "1" {
        Write-Host "`n→ Ejecutando demo completa..." -ForegroundColor Yellow
        python demo_sistema_completo.py
    }
    "2" {
        Write-Host "`n→ Iniciando modo interactivo..." -ForegroundColor Yellow
        python demo_sistema_completo.py --interactivo
    }
    "3" {
        if (-not $configLista) {
            Write-Host "`n✗ Configuración incompleta. Configurar variables de entorno primero." -ForegroundColor Red
            exit 1
        }

        Write-Host "`n→ Implementando en Dataverse..." -ForegroundColor Yellow
        python implementar_todo.py

        if ($LASTEXITCODE -eq 0) {
            Write-Host "`n→ Ejecutando demo..." -ForegroundColor Yellow
            python demo_sistema_completo.py
        } else {
            Write-Host "`n✗ Error en implementación. Abortando." -ForegroundColor Red
            exit 1
        }
    }
    "4" {
        if (-not $configLista) {
            Write-Host "`n✗ Configuración incompleta. Configurar variables de entorno primero." -ForegroundColor Red
            exit 1
        }

        Write-Host "`n→ Implementando en Dataverse..." -ForegroundColor Yellow
        python implementar_todo.py
    }
    default {
        Write-Host "`n✗ Opción inválida" -ForegroundColor Red
        exit 1
    }
}

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "FIN DE EJECUCIÓN" -ForegroundColor Cyan
Write-Host "============================================================" -ForegroundColor Cyan
