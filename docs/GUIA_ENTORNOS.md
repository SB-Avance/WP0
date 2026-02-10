# 🚀 Guía Rápida - Cambio de Entorno

## 📋 Comandos Disponibles

### 🔄 Cambiar Entorno (Menú Interactivo)
```powershell
.\cambiar_entorno.ps1
```
Muestra un menú para seleccionar entre LOCAL, AZURE o PRODUCTION.

### 🔄 Cambiar Entorno (Directo)
```powershell
.\cambiar_entorno.ps1 LOCAL      # Usar backend local
.\cambiar_entorno.ps1 AZURE      # Usar backend en Azure
.\cambiar_entorno.ps1 PRODUCTION # Usar backend en producción
```

### ▶️ Iniciar Aplicación
```powershell
.\iniciar.ps1                # Usa el entorno guardado
.\iniciar.ps1 LOCAL          # Inicia con backend LOCAL
.\iniciar.ps1 AZURE          # Inicia con backend AZURE
```

### 🖥️ Iniciar Backend Local
```powershell
.\iniciar_backend.ps1
```
Inicia el servidor Flask en `http://localhost:5000`

### 🔄 Sincronizar con GitHub
```powershell
.\sync.ps1 "Mensaje del commit"
```
Detiene procesos Python, hace commit y push automático.

---

## 🎯 Flujos de Trabajo Comunes

### Trabajar en LOCAL
```powershell
# Terminal 1: Backend
.\iniciar_backend.ps1

# Terminal 2: Frontend
.\iniciar.ps1 LOCAL
```

### Trabajar con AZURE
```powershell
# Solo necesitas una terminal
.\iniciar.ps1 AZURE
```

### Cambiar de entorno
```powershell
# Opción 1: Menú interactivo
.\cambiar_entorno.ps1

# Opción 2: Directo
.\cambiar_entorno.ps1 AZURE
.\iniciar.ps1
```

---

## ⚙️ Configuración de Entornos

Los entornos se configuran en `mobile/config.py`:

- **LOCAL**: `http://localhost:5000`
- **AZURE**: `https://whatsapp-flask-app-f4gsb7dhhybcg6f6.eastus-01.azurewebsites.net`
- **PRODUCTION**: Se configura con variable `PRODUCTION_URL`

El entorno actual se guarda en:
- Variable de entorno del sistema: `ENVIRONMENT`
- Archivo temporal: `.env_state`

---

## 📝 Notas

- El cambio de entorno persiste entre sesiones
- `.\iniciar.ps1` recuerda el último entorno usado
- Los scripts detienen automáticamente procesos Python previos
