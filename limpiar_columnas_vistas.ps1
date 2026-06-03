# ================================================================
# Script para quitar columnas específicas de vistas en Dataverse
# ================================================================
# USO: Editar $columnasAQuitar y $tabla, luego ejecutar
# NOTA: Requiere permisos de administrador en Power Apps
# ================================================================

Write-Host "`n╔════════════════════════════════════════════╗" -ForegroundColor Cyan
Write-Host "║  LIMPIAR COLUMNAS DE VISTAS - DATAVERSE   ║" -ForegroundColor Cyan
Write-Host "╚════════════════════════════════════════════╝`n" -ForegroundColor Cyan

# ============ CONFIGURACIÓN ============

# Power Platform CLI debe estar instalado:
# winget install Microsoft.PowerPlatformCLI

# Tabla a modificar
$tabla = "cr321_usuarios"  # Cambiar según tu tabla

# Columnas que quieres quitar de las vistas
$columnasAQuitar = @(
    "cr321_1",
    "cr321_3",
    "cr321_4",
    "cr321_usuariogrupo1"
    # Agregar más columnas aquí
)

# ============ FUNCIONES ============

function Show-Instructions {
    Write-Host "PASOS MANUALES (mientras tanto):`n" -ForegroundColor Yellow

    Write-Host "1. Ve a: " -NoNewline -ForegroundColor White
    Write-Host "https://make.powerapps.com" -ForegroundColor Cyan

    Write-Host "`n2. Navega a:" -ForegroundColor White
    Write-Host "   Tablas → " -NoNewline -ForegroundColor Gray
    Write-Host "$tabla" -NoNewline -ForegroundColor Yellow
    Write-Host " → Pestaña 'Vistas'" -ForegroundColor Gray

    Write-Host "`n3. Para CADA vista:" -ForegroundColor White
    Write-Host "   • Abrir editor de vista" -ForegroundColor Gray
    Write-Host "   • Buscar y quitar estas columnas:" -ForegroundColor Gray

    foreach ($col in $columnasAQuitar) {
        Write-Host "     ✗ $col" -ForegroundColor Red
    }

    Write-Host "   • Guardar y Publicar" -ForegroundColor Gray

    Write-Host "`n4. Repetir para la pestaña 'Formularios'" -ForegroundColor White

    Write-Host "`n═══════════════════════════════════════════`n" -ForegroundColor Cyan
}

function Hide-ColumnFromSearch {
    param($columnName)

    Write-Host "`n⚠️ Para ocultar '$columnName' de búsquedas:" -ForegroundColor Yellow
    Write-Host "   1. Tablas → $tabla → Columnas" -ForegroundColor Gray
    Write-Host "   2. Buscar: $columnName" -ForegroundColor Gray
    Write-Host "   3. ⋮ → Editar → Opciones avanzadas" -ForegroundColor Gray
    Write-Host "   4. DESACTIVAR: 'Aparece en búsquedas globales'" -ForegroundColor Gray
    Write-Host "   5. Guardar`n" -ForegroundColor Gray
}

# ============ EJECUCIÓN ============

Show-Instructions

Write-Host "¿Deseas ver instrucciones para ocultar columnas de búsquedas? (s/n): " -NoNewline -ForegroundColor Yellow
$respuesta = Read-Host

if ($respuesta -eq "s" -or $respuesta -eq "S") {
    foreach ($col in $columnasAQuitar) {
        Hide-ColumnFromSearch $col
    }
}

Write-Host "`n✅ Guía completada" -ForegroundColor Green
Write-Host "💡 TIP: Marca columnas como 'DEPRECATED' en descripción si no puedes eliminarlas`n" -ForegroundColor Cyan

# ============ NOTAS ============
<#
ALTERNATIVA CON POWER PLATFORM CLI (Requiere configuración adicional):

pac auth create --url https://[tu-entorno].crm.dynamics.com
pac solution export --name [NombreSolucion] --path ./temp --managed false
# Editar customizations.xml (remover columnas de vistas)
pac solution import --path ./temp

NOTA: Esto es complejo y requiere conocimiento de XML de soluciones.
      La opción manual en Power Apps es más rápida y segura.
#>
