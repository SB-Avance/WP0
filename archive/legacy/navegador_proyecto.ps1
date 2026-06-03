# ========================================
# NAVEGADOR DE PROYECTO - Sistema de Menu JSON
# ========================================
# Este script ayuda a navegar el proyecto y evitar archivos historicos

[CmdletBinding()]
param(
    [switch]$VerDocumentos,
    [switch]$VerScripts,
    [switch]$VerHistoricos,
    [switch]$Ayuda
)

# Configurar codificacion para caracteres especiales
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

function Show-Header {
    Write-Host "`n========================================" -ForegroundColor Cyan
    Write-Host "   NAVEGADOR DE PROYECTO - Menu JSON" -ForegroundColor Cyan
    Write-Host "========================================`n" -ForegroundColor Cyan
}

function Show-QuickStart {
    Write-Host "⚡ INICIO RAPIDO:" -ForegroundColor Yellow
    Write-Host "  1. Demo local (sin Dataverse):" -ForegroundColor White
    Write-Host "     python demo_local.py`n" -ForegroundColor Green
    Write-Host "  2. Demo interactiva:" -ForegroundColor White
    Write-Host "     python demo_local.py --interactivo`n" -ForegroundColor Green
    Write-Host "  3. Implementar en Dataverse:" -ForegroundColor White
    Write-Host "     python implementar_todo.py`n" -ForegroundColor Green
}

function Show-Documents {
    Write-Host "`n📚 DOCUMENTOS ACTUALES (Usar estos):" -ForegroundColor Green
    Write-Host "  ⭐⭐⭐ EMPEZAR_AQUI.md" -ForegroundColor Cyan
    Write-Host "         └─ Demo en 2 minutos`n" -ForegroundColor Gray

    Write-Host "  ⭐⭐ README_INICIO_RAPIDO.md" -ForegroundColor Cyan
    Write-Host "       └─ Arquitectura simple explicada`n" -ForegroundColor Gray

    Write-Host "  ⭐ GUIA_IMPLEMENTACION_JSON.md" -ForegroundColor Cyan
    Write-Host "     └─ Guia paso a paso completa`n" -ForegroundColor Gray

    Write-Host "  📋 RESUMEN_IMPLEMENTACION_COMPLETA.md" -ForegroundColor Cyan
    Write-Host "     └─ Estado del proyecto`n" -ForegroundColor Gray

    Write-Host "  ⚠️ ACLARACION_ARCHIVOS_HISTORICOS.md" -ForegroundColor Yellow
    Write-Host "     └─ Que archivos usar y cuales evitar`n" -ForegroundColor Gray

    Write-Host "  ⚠️ ADVERTENCIA_ARCHIVOS_HISTORICOS.txt" -ForegroundColor Yellow
    Write-Host "     └─ Lista de campos que NO existen`n" -ForegroundColor Gray
}

function Show-Scripts {
    Write-Host "`n🔧 SCRIPTS PRINCIPALES:" -ForegroundColor Green
    Write-Host "  ✅ demo_local.py" -ForegroundColor Cyan
    Write-Host "     └─ Demo sin Dataverse (RECOMENDADO)"`n -ForegroundColor Gray

    Write-Host "  ✅ sistema_menu_json.py" -ForegroundColor Cyan
    Write-Host "     └─ Sistema principal con JSON`n" -ForegroundColor Gray

    Write-Host "  ✅ implementar_todo.py" -ForegroundColor Cyan
    Write-Host "     └─ Deploy automatico a Dataverse`n" -ForegroundColor Gray

    Write-Host "  ✅ validar_grupos_menu.py" -ForegroundColor Cyan
    Write-Host "     └─ Validar grupo_id contra Dataverse`n" -ForegroundColor Gray

    Write-Host "  ✅ gestionar_chatbots.py" -ForegroundColor Cyan
    Write-Host "     └─ Activar/desactivar chatbots`n" -ForegroundColor Gray

    Write-Host "  📄 JSON_LISTO_PARA_INSERTAR.json" -ForegroundColor Cyan
    Write-Host "     └─ Configuracion completa del menu`n" -ForegroundColor Gray
}

function Show-HistoricalFiles {
    Write-Host "`n❌ ARCHIVOS HISTORICOS (NO usar para implementar):" -ForegroundColor Red
    Write-Host "  ⚠️ ANALISIS_ARQUITECTURA_HANDLERS.md" -ForegroundColor Yellow
    Write-Host "     └─ Analisis de 4 opciones (solo referencia)`n" -ForegroundColor Gray

    Write-Host "  ⚠️ COMPARATIVA_OPCIONES_HANDLERS.md" -ForegroundColor Yellow
    Write-Host "     └─ Comparacion de opciones (solo referencia)`n" -ForegroundColor Gray

    Write-Host "  ⚠️ RESUMEN_EJECUTIVO_HANDLERS.md" -ForegroundColor Yellow
    Write-Host "     └─ Resumen ejecutivo de opciones (solo referencia)`n" -ForegroundColor Gray

    Write-Host "  ⚠️ ACLARACION_INDEPENDENCIA_HANDLER_ELEMENTO.md" -ForegroundColor Yellow
    Write-Host "     └─ Aclaracion de arquitectura (solo referencia)`n" -ForegroundColor Gray

    Write-Host "`n  ⚠️ ESTOS ARCHIVOS MENCIONAN CAMPOS QUE NO EXISTEN:" -ForegroundColor Red
    Write-Host "     - cr321_elemento1, cr321_elemento2, etc." -ForegroundColor Yellow
    Write-Host "     - cr321_grupo1, cr321_grupo2, etc." -ForegroundColor Yellow
    Write-Host "     - cr321_orden" -ForegroundColor Yellow
    Write-Host "     - cr321_handler1, cr321_handler2, etc.`n" -ForegroundColor Yellow
}

function Show-CurrentArchitecture {
    Write-Host "`n✅ ARQUITECTURA ACTUAL (Implementada):" -ForegroundColor Green
    Write-Host "  📊 Tabla cr321_chatbots:" -ForegroundColor Cyan
    Write-Host "     ├─ cr321_config  (texto 100KB) ← TODO el JSON aqui" -ForegroundColor White
    Write-Host "     ├─ cr321_active  (booleano)" -ForegroundColor White
    Write-Host "     └─ cr321_name    (texto)`n" -ForegroundColor White

    Write-Host "  📊 Tabla cr321_grupos:" -ForegroundColor Cyan
    Write-Host "     ├─ cr321_grupoid (GUID - Primary Key)" -ForegroundColor White
    Write-Host "     ├─ cr321_codigo  (texto: 0000, 0001, etc.)" -ForegroundColor White
    Write-Host "     └─ cr321_nombre  (texto: General, Soporte, etc.)`n" -ForegroundColor White

    Write-Host "  📊 JSON en cr321_config contiene:" -ForegroundColor Cyan
    Write-Host "     ├─ menus[] - Lista de menus principales" -ForegroundColor White
    Write-Host "     │   ├─ opcion (texto: '1', '2', etc.)" -ForegroundColor Gray
    Write-Host "     │   ├─ texto_opcion (texto a mostrar)" -ForegroundColor Gray
    Write-Host "     │   ├─ handler (nombre del archivo py)" -ForegroundColor Gray
    Write-Host "     │   ├─ grupo_id (GUID de cr321_grupos)" -ForegroundColor Gray
    Write-Host "     │   └─ submenus[] (opcional)" -ForegroundColor Gray
    Write-Host "     │       ├─ subopcion ('1.1', '1.2', etc.)" -ForegroundColor DarkGray
    Write-Host "     │       ├─ texto_opcion" -ForegroundColor DarkGray
    Write-Host "     │       ├─ handler" -ForegroundColor DarkGray
    Write-Host "     │       └─ grupo_id (GUID)" -ForegroundColor DarkGray
    Write-Host "     └─ mensaje_bienvenida (texto)`n" -ForegroundColor White
}

function Show-Menu {
    Show-Header

    Write-Host "Opciones:" -ForegroundColor White
    Write-Host "  1. Inicio rapido (comandos basicos)" -ForegroundColor Cyan
    Write-Host "  2. Ver documentos actuales" -ForegroundColor Cyan
    Write-Host "  3. Ver scripts principales" -ForegroundColor Cyan
    Write-Host "  4. Ver arquitectura actual" -ForegroundColor Cyan
    Write-Host "  5. Ver archivos historicos (que NO usar)" -ForegroundColor Yellow
    Write-Host "  6. Ejecutar demo local" -ForegroundColor Green
    Write-Host "  7. Ejecutar demo interactiva" -ForegroundColor Green
    Write-Host "  8. Abrir EMPEZAR_AQUI.md" -ForegroundColor Cyan
    Write-Host "  0. Salir`n" -ForegroundColor Red

    $opcion = Read-Host "Selecciona una opcion"

    switch ($opcion) {
        "1" {
            Clear-Host
            Show-QuickStart
            Write-Host "`nPresiona Enter para continuar..." -ForegroundColor Gray
            Read-Host
            Show-Menu
        }
        "2" {
            Clear-Host
            Show-Documents
            Write-Host "`nPresiona Enter para continuar..." -ForegroundColor Gray
            Read-Host
            Show-Menu
        }
        "3" {
            Clear-Host
            Show-Scripts
            Write-Host "`nPresiona Enter para continuar..." -ForegroundColor Gray
            Read-Host
            Show-Menu
        }
        "4" {
            Clear-Host
            Show-CurrentArchitecture
            Write-Host "`nPresiona Enter para continuar..." -ForegroundColor Gray
            Read-Host
            Show-Menu
        }
        "5" {
            Clear-Host
            Show-HistoricalFiles
            Write-Host "`nPresiona Enter para continuar..." -ForegroundColor Gray
            Read-Host
            Show-Menu
        }
        "6" {
            Clear-Host
            Write-Host "`nEjecutando demo local...`n" -ForegroundColor Green
            python demo_local.py
  Funcion principal
function Main {
    # Si se pasan parametros, usa modo no interactivo
    if ($VerDocumentos) {
        Show-Header
        Show-Documents
        return
    }

    if ($VerScripts) {
        Show-Header
        Show-Scripts
        return
    }

    if ($VerHistoricos) {
        Show-Header
        Show-HistoricalFiles
        return
    }

    if ($Ayuda) {
        Show-Header
        Write-Host "USO:" -ForegroundColor Yellow
        Write-Host "  .\navegador_proyecto.ps1                   # Modo interactivo (menu)" -ForegroundColor White
        Write-Host "  .\navegador_proyecto.ps1 -VerDocumentos    # Ver documentos actuales" -ForegroundColor White
        Write-Host "  .\navegador_proyecto.ps1 -VerScripts       # Ver scripts principales" -ForegroundColor White
        Write-Host "  .\navegador_proyecto.ps1 -VerHistoricos    # Ver archivos historicos" -ForegroundColor White
        Write-Host "  .\navegador_proyecto.ps1 -Ayuda            # Esta ayuda`n" -ForegroundColor White
        return
    }

    # Modo interactivo (menu)
    Clear-Host
    Show-Menu
}

# Ejecutar funcion principal
Main   Show-Menu
        }
    }
}

# Si se pasan parametros, usa modo no interactivo
if ($VerDocumentos) {
    Show-Header
    Show-Documents
    exit
}

if ($VerScripts) {
    Show-Header
    Show-Scripts
    exit
}

if ($VerHistoricos) {
    Show-Header
    Show-HistoricalFiles
    exit
}

if ($Ayuda) {
    Show-Header
    Write-Host "USO:" -ForegroundColor Yellow
    Write-Host "  .\navegador_proyecto.ps1              # Modo interactivo (menu)" -ForegroundColor White
    Write-Host "  .\navegador_proyecto.ps1 -VerDocumentos    # Ver documentos actuales" -ForegroundColor White
    Write-Host "  .\navegador_proyecto.ps1 -VerScripts       # Ver scripts principales" -ForegroundColor White
    Write-Host "  .\navegador_proyecto.ps1 -VerHistoricos    # Ver archivos historicos" -ForegroundColor White
    Write-Host "  .\navegador_proyecto.ps1 -Ayuda           # Esta ayuda`n" -ForegroundColor White
    exit
}

# Modo interactivo (menu)
Show-Menu
