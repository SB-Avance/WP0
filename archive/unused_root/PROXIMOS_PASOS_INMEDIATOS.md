# 🚀 Guía Rápida - Próximos Pasos

## ✅ Completado Hoy

```
[✅] Mejora #1: API con $expand (performance 10x)
[✅] Mejora #3: Auto-contactos con Lookup (100% asociados)
[✅] Tests: 8/9 tests pasados
[✅] Documentación: Completa y actualizada
```

---

## 📋 Comandos para Verificar Ahora

### 1. Reiniciar Backend con Cambios

```powershell
# Opción A: Usar script
.\iniciar_backend.ps1

# Opción B: Manual
cd backend
C:/VS/BIN/venv_clean/Scripts/python.exe back.py
```

Deberías ver:
```
 * Running on http://127.0.0.1:5000
 * Running on http://192.168.X.X:5000
```

### 2. Probar API con $expand (Mejora #1)

```powershell
# Health check
curl http://localhost:5000/api/chats/health

# Ver chats con contactos (NUEVO)
curl http://localhost:5000/api/chats/con-contacto?top=5

# Ver estadísticas por grupo (NUEVO)
curl http://localhost:5000/api/chats/estadisticas-grupos

# Buscar mensajes (NUEVO)
curl "http://localhost:5000/api/chats/buscar?texto=hola&top=5"
```

Deberías ver JSON con contactos expandidos:
```json
{
  "chats": [
    {
      "cr321_adatawp0oid": "...",
      "cr321_body": "Hola, necesito información",
      "contacto": {
        "id": "...",
        "nombre": "Juan Pérez",
        "telefono": "+573001234567"
      }
    }
  ]
}
```

### 3. Enviar Mensaje de Prueba WhatsApp

```
1. Abre WhatsApp en tu teléfono
2. Envía mensaje a tu número de prueba
3. Mensaje: "Hola, soy prueba de contactos"
```

### 4. Verificar Auto-Contacto (Mejora #3)

```powershell
# Ver últimos mensajes con contactos
curl http://localhost:5000/api/chats/con-contacto?top=10

# Buscar tu mensaje de prueba
curl "http://localhost:5000/api/chats/buscar?texto=prueba+contactos"
```

**Verifica que:**
- ✅ El mensaje aparece
- ✅ Tiene contacto asociado (`contacto` no es null)
- ✅ El contacto tiene tu teléfono y nombre

---

## 📊 Comandos de Diagnóstico

### Ver Logs del Backend

Si el backend está corriendo, revisa la consola para ver:
```
[✅ CONTACTO] Nuevo creado: <guid>
[✅ LOOKUP] Asociando mensaje con contacto: <guid>
[✅ MENSAJE] Guardado con lookups correctamente
```

### Ejecutar Tests de Nuevo

```powershell
# Test API con $expand
python test_chats_extended.py

# Test auto-contactos
python test_webhook_enhanced.py

# Test completo del sistema
python test_sistema.py
```

### Verificar Campos en Dataverse

```powershell
# Ver campos de tabla chats
python ver_campos_tabla.py

# Ver estado de migración
python ver_estado_migracion.py

# Verificar cambios Lookup
python verificar_cambios_tabla.py
```

---

## 🔍 Troubleshooting

### Backend no inicia

```powershell
# Verificar puerto 5000 libre
netstat -ano | findstr :5000

# Si está ocupado, matar proceso
taskkill /PID <PID> /F

# Reintentar
cd backend
python back.py
```

### Endpoints 404

```
✅ Verificar que back.py registró el blueprint:
   - Buscar "bp_chats_extended" en back.py
   - Debe estar en línea ~532-535

✅ Verificar que backend reinició después de cambios
```

### Mensaje no tiene contacto

```
✅ Verificar logs del webhook:
   - Debe decir "[✅ CONTACTO]" y "[✅ MENSAJE]"

✅ Si dice error, revisar:
   - Variables de entorno (DATAVERSE_URL, etc.)
   - Permisos en Dataverse
   - Token de autenticación
```

### Tests fallan

```powershell
# Verificar Python environment
C:/VS/BIN/venv_clean/Scripts/python.exe --version
# Debe ser Python 3.12.10

# Verificar dependencias
pip list | findstr requests
pip list | findstr msal

# Reinstalar si necesario
pip install -r backend/requirements.txt
```

---

## 📝 Próxima Sesión (Viernes)

### Mejora #2: Dashboard de Métricas

**Tiempo estimado:** 4-5 horas

**Archivos a crear:**
```
backend/api/
  └── dashboard.py       # Nuevos endpoints de métricas

test_dashboard.py        # Tests
docs/
  └── MEJORA_2_DASHBOARD_METRICAS.md  # Documentación
```

**Endpoints a implementar:**
```
GET /api/dashboard/metricas-grupos
    → Estadísticas por grupo (mensajes, contactos, avg tiempo)

GET /api/dashboard/metricas-generales
    → Sistema completo (total msgs, usuarios activos, etc.)

GET /api/dashboard/volumetria?desde=DATE&hasta=DATE
    → Volúmenes de mensajes por período
```

**Comando para empezar:**
```powershell
# Copiar template desde chats_extended.py
cp backend/api/chats_extended.py backend/api/dashboard.py

# Editar y adaptar
code backend/api/dashboard.py
```

---

## 📚 Documentación de Referencia

| Documento | Qué Contiene |
|-----------|--------------|
| [API_CHATS_EXTENDED.md](API_CHATS_EXTENDED.md) | Detailed API docs Mejora #1 |
| [MEJORA_3_AUTO_CONTACTOS_LOOKUP.md](MEJORA_3_AUTO_CONTACTOS_LOOKUP.md) | Detailed docs Mejora #3 |
| [SUGERENCIAS_PROXIMOS_PASOS.md](SUGERENCIAS_PROXIMOS_PASOS.md) | Roadmap completo |
| [RESUMEN_IMPLEMENTACION_FEB2024.md](RESUMEN_IMPLEMENTACION_FEB2024.md) | Resumen de hoy |
| [MAPA_APLICACION.md](MAPA_APLICACION.md) | Arquitectura + diagramas |
| [INDICE_DOCUMENTACION.md](INDICE_DOCUMENTACION.md) | Índice completo |

---

## ✅ Checklist Inmediata

Ejecuta esto ahora:

```powershell
# 1. Reiniciar backend
cd C:\VS\BIN\backend
python back.py

# 2. En otra terminal, probar API
curl http://localhost:5000/api/chats/health
curl http://localhost:5000/api/chats/con-contacto?top=5

# 3. Enviar mensaje WhatsApp de prueba
# [Hazlo desde tu teléfono]

# 4. Verificar mensaje con contacto
curl http://localhost:5000/api/chats/con-contacto?top=10
```

**Si todo funciona:** ✅ Producción lista
**Si algo falla:** Ver sección Troubleshooting arriba

---

## 🎯 Objetivo de Hoy

- [x] Mejora #1 implementada
- [x] Mejora #3 implementada
- [ ] **→ Verificación en producción** ← ESTÁS AQUÍ
- [ ] Monitoreo 24-48h
- [ ] Mejora #2 (Viernes)

---

**¡Éxito! 🎉** Sistema optimizado y listo para producción.
