# Script PowerShell para crear tablas en Dataverse
# Requiere: Microsoft.PowerApps.Administration.PowerShell

<#
.SYNOPSIS
Script para crear las tablas necesarias del sistema de chatbot WhatsApp en Dataverse

.DESCRIPTION
Crea las siguientes tablas:
- cr321_grupos
- cr321_estados  
- cr321_tickets
- cr321_usuario_grupos

.NOTES
Antes de ejecutar:
1. Install-Module -Name Microsoft.PowerApps.Administration.PowerShell
2. Connect-DataverseEnvironment -EnvironmentUrl "https://tu-entorno.crm.dynamics.com"
#>

# Configuración
$environmentUrl = "https://tu-entorno.crm.dynamics.com"
$prefix = "cr321_"

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "  CREACIÓN DE TABLAS EN DATAVERSE" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

# Nota: Este script es una GUÍA. Las tablas deben crearse en Power Platform Admin Center
# o usando la API Web de Dataverse con solicitudes HTTP

Write-Host "INSTRUCCIONES PARA CREAR TABLAS EN DATAVERSE" -ForegroundColor Yellow
Write-Host ""

Write-Host "================================================" -ForegroundColor Green
Write-Host "1. TABLA: cr321_grupos" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "Nombre de visualización: Grupos"
Write-Host "Nombre plural: Grupos"
Write-Host ""
Write-Host "CAMPOS:" -ForegroundColor White
Write-Host "  - cr321_idgrupo (Tipo: Número entero, Obligatorio)"
Write-Host "  - cr321_nombre (Tipo: Texto, Longitud: 100, Obligatorio)"
Write-Host "  - cr321_tipo (Tipo: Conjunto de opciones)"
Write-Host "      462410000 = Tipo A"
Write-Host "      462410001 = Tipo B"
Write-Host "      462410002 = Tipo C"
Write-Host "  - cr321_descripcion (Tipo: Texto, Longitud: 500)"
Write-Host ""

Write-Host "================================================" -ForegroundColor Green
Write-Host "2. TABLA: cr321_estados" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "Nombre de visualización: Estados"
Write-Host "Nombre plural: Estados"
Write-Host ""
Write-Host "CAMPOS:" -ForegroundColor White
Write-Host "  - cr321_idestado (Tipo: Número entero, Obligatorio)"
Write-Host "  - cr321_nombre (Tipo: Texto, Longitud: 100, Obligatorio)"
Write-Host "  - cr321_descripcion (Tipo: Texto, Longitud: 500)"
Write-Host ""

Write-Host "================================================" -ForegroundColor Green
Write-Host "3. TABLA: cr321_tickets" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "Nombre de visualización: Tickets"
Write-Host "Nombre plural: Tickets"
Write-Host ""
Write-Host "CAMPOS:" -ForegroundColor White
Write-Host "  - cr321_idticket (Tipo: Número entero, Obligatorio)"
Write-Host "  - cr321_fromnombre (Tipo: Texto, Longitud: 100, Obligatorio)"
Write-Host "  - cr321_telefono (Tipo: Texto, Longitud: 20, Obligatorio)"
Write-Host "  - cr321_empresa (Tipo: Texto, Longitud: 200)"
Write-Host "  - cr321_descripcion (Tipo: Texto multilínea, Longitud: 2000)"
Write-Host "  - cr321_tipo (Tipo: Conjunto de opciones)"
Write-Host "      462410000 = Soporte"
Write-Host "      462410001 = Cotización"
Write-Host "      462410002 = Información"
Write-Host "      462410003 = Atención Agente"
Write-Host "  - cr321_estado (Tipo: Número entero)"
Write-Host "  - cr321_grupoid (Tipo: Búsqueda, Tabla: cr321_grupos)"
Write-Host "  - cr321_fechacreacion (Tipo: Fecha y hora)"
Write-Host "  - cr321_fechaactualizacion (Tipo: Fecha y hora)"
Write-Host ""

Write-Host "================================================" -ForegroundColor Green
Write-Host "4. TABLA: cr321_usuario_grupos" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host "Nombre de visualización: Usuario Grupos"
Write-Host "Nombre plural: Usuario Grupos"
Write-Host ""
Write-Host "CAMPOS:" -ForegroundColor White
Write-Host "  - cr321_usuarioid (Tipo: Búsqueda, Tabla: cr321_usuarios)"
Write-Host "  - cr321_grupoid (Tipo: Búsqueda, Tabla: cr321_grupos)"
Write-Host ""

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "PASOS PARA CREAR LAS TABLAS:" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "1. Ir a Power Apps (https://make.powerapps.com)" -ForegroundColor White
Write-Host "2. Seleccionar tu entorno"
Write-Host "3. En el menú lateral, ir a 'Tablas'"
Write-Host "4. Hacer clic en '+ Nueva tabla' > 'Crear tabla'"
Write-Host "5. Para cada tabla arriba:"
Write-Host "   a. Ingresar nombre y crear la tabla"
Write-Host "   b. Agregar los campos listados"
Write-Host "   c. Para campos de Conjunto de opciones, crear las opciones con los valores especificados"
Write-Host "   d. Para campos de Búsqueda, seleccionar la tabla relacionada"
Write-Host "6. Guardar y publicar cada tabla"
Write-Host ""

Write-Host "================================================" -ForegroundColor Yellow
Write-Host "ALTERNATIVA: Usar API Web de Dataverse" -ForegroundColor Yellow
Write-Host "================================================" -ForegroundColor Yellow
Write-Host ""
Write-Host "Para crear tablas programáticamente, usar solicitudes HTTP POST a:" -ForegroundColor White
Write-Host "  $environmentUrl/api/data/v9.2/EntityDefinitions"
Write-Host ""
Write-Host "Ejemplo JSON para crear tabla (ver documentación de Microsoft):" -ForegroundColor White
Write-Host @"
{
  "SchemaName": "cr321_grupos",
  "DisplayName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Grupos", "LanguageCode": 1033}] },
  "DisplayCollectionName": { "@odata.type": "Microsoft.Dynamics.CRM.Label", "LocalizedLabels": [{"@odata.type": "Microsoft.Dynamics.CRM.LocalizedLabel", "Label": "Grupos", "LanguageCode": 1033}] },
  "OwnershipType": "UserOwned",
  "HasActivities": false,
  "IsActivity": false
}
"@
Write-Host ""

Write-Host "================================================" -ForegroundColor Green
Write-Host "DESPUÉS DE CREAR LAS TABLAS:" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "1. Ejecutar script de inicialización:" -ForegroundColor White
Write-Host "   python init_dataverse.py"
Write-Host ""
Write-Host "2. Asignar usuarios a grupos:" -ForegroundColor White
Write-Host "   POST /api/usuario-grupos"
Write-Host ""
Write-Host "3. Configurar webhook de WhatsApp"
Write-Host ""
Write-Host "4. Iniciar el backend:" -ForegroundColor White
Write-Host "   python backend/back.py"
Write-Host ""

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "SCRIPT COMPLETADO" -ForegroundColor Cyan
Write-Host "================================================" -ForegroundColor Cyan
