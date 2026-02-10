# Tests del Sistema

Esta carpeta contiene todos los tests del sistema de chatbot Dataverse.

## Tests Disponibles

### Backend API
- `test_backend.py` - Tests básicos del backend Flask
- `test_chats_extended.py` - Tests de API extendida de chats (Mejora #1)
- `test_dashboard.py` - Tests de dashboard de métricas (Mejora #2)

### Webhooks
- `test_webhook_contacto.py` - Tests del webhook de contactos
- `test_webhook_enhanced.py` - Tests del webhook mejorado con lookup (Mejora #3)

### Sistema
- `test_sistema.py` - Tests del sistema completo
- `test_campo_lookup.py` - Tests de campos lookup

## Ejecutar Tests

### Requisitos
Asegurarse de tener el entorno virtual activado y el backend corriendo:
```powershell
# Activar entorno virtual
.\venv_clean\Scripts\Activate.ps1

# Iniciar backend (en otra terminal)
python backend/back.py
```

### Ejecutar Tests Individuales
```powershell
# Mejora #1 - API con $expand
python tests/test_chats_extended.py

# Mejora #2 - Dashboard
python tests/test_dashboard.py

# Mejora #3 - Webhook mejorado
python tests/test_webhook_enhanced.py

# Sistema completo
python tests/test_sistema.py
```

### Ejecutar Todos los Tests
```powershell
Get-ChildItem tests/*.py | ForEach-Object { python $_.FullName }
```

## Resultados Esperados

### Mejora #1 (test_chats_extended.py)
- ✅ 4/5 tests pasando
- Cobertura: Health, con-contacto, estadísticas-grupos, buscar

### Mejora #2 (test_dashboard.py)
- ⚠️ 3/5 tests pasando
- Conocido: Timeout en métricas-grupos, falta data en volumetría/tendencias

### Mejora #3 (test_webhook_enhanced.py)
- ✅ 4/4 tests pasando
- Cobertura: Crear contacto, asociación automática, validaciones

### Total Sistema
- ✅ 11/13 tests pasando (85%)

## Notas

- Backend debe estar corriendo en `http://localhost:5000`
- Algunos tests requieren datos en Dataverse
- Ver `../docs/VALIDACION_SISTEMA_FEB2026.md` para detalles

**Última actualización:** 2026-02-08
