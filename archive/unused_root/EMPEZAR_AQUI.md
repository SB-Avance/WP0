# 🚀 EMPIEZA AQUÍ - Sistema de Chatbot con Menú JSON

## ⚡ Inicio en 2 minutos

### Opción 1: Demo Local (SIN necesidad de configurar nada)
```powershell
python demo_local.py
```

¿Qué hace esto?
- ✅ Carga el sistema de menú desde JSON
- ✅ Simula WhatsApp completamente
- ✅ NO necesita Dataverse
- ✅ NO necesita credenciales
- ✅ Funciona AHORA MISMO

### Opción 2: Modo Interactivo (Probar tú mismo)
```powershell
python demo_local.py --interactivo
```

Prueba comandos como:
- `Hola` → Ver menú principal
- `1` → Opción 1 (Soporte Técnico)
- `1.1` → Subopción directa
- `menu` → Volver al menú
- `salir` → Terminar

---

## 📚 ¿Qué leer después?

### Si quieres entender el sistema:
1. [README_INICIO_RAPIDO.md](README_INICIO_RAPIDO.md) ⭐ - Arquitectura simple explicada
2. [GUIA_IMPLEMENTACION_JSON.md](GUIA_IMPLEMENTACION_JSON.md) - Guía paso a paso

### Si quieres implementar en Dataverse:
1. Configurar credenciales en `.env`
2. Ejecutar: `python implementar_todo.py`
3. Validar: `python validar_grupos_menu.py`

### Si ves referencias a cr321_elemento1, cr321_grupo1, etc:
1. ⚠️ **NO LOS USES** - Son de análisis histórico
2. Lee: [ACLARACION_ARCHIVOS_HISTORICOS.md](ACLARACION_ARCHIVOS_HISTORICOS.md)
3. Ver: [ADVERTENCIA_ARCHIVOS_HISTORICOS.txt](ADVERTENCIA_ARCHIVOS_HISTORICOS.txt)

---

## ❌ Lo que NO necesitas hacer

- ❌ NO crear campos cr321_elemento1, cr321_elemento2, etc.
- ❌ NO crear campos cr321_grupo1, cr321_grupo2, etc.
- ❌ NO crear campo cr321_orden
- ❌ NO leer archivos que empiezan con "ANALISIS_" o "COMPARATIVA_"

---

## ✅ Lo que SÍ necesitas

### En Dataverse (cuando estés listo):
Solo 3 campos en tabla `cr321_chatbots`:
1. `cr321_config` (tipo: texto, tamaño: 100KB) ← Aquí va TODO
2. `cr321_active` (tipo: booleano)
3. `cr321_name` (tipo: texto)

### En tu sistema:
- Python 3.7+
- Archivo: `JSON_LISTO_PARA_INSERTAR.json` (ya existe)
- Tabla: `cr321_grupos` con tus grupos (ya tienes 5 grupos)

---

## 🎯 Flujo recomendado

### Día 1: Entender el sistema
```powershell
# 1. Probar demo local
python demo_local.py

# 2. Probar modo interactivo
python demo_local.py --interactivo

# 3. Ver el JSON configurado
notepad JSON_LISTO_PARA_INSERTAR.json
```

### Día 2: Implementar
```powershell
# 1. Configurar credenciales
notepad .env

# 2. Implementar automáticamente
python implementar_todo.py

# 3. Validar
python validar_grupos_menu.py
```

### Día 3: Personalizar
```powershell
# 1. Editar JSON_LISTO_PARA_INSERTAR.json
# 2. Agregar nuevos handlers en handlers/
# 3. Volver a implementar
python implementar_todo.py
```

---

## 📖 Documentos clave

| Documento | Para qué sirve | Cuándo leerlo |
|-----------|----------------|---------------|
| **EMPEZAR_AQUI.md** | Esta guía | AHORA |
| **README_INICIO_RAPIDO.md** | Explicación simple | Después de la demo |
| **GUIA_IMPLEMENTACION_JSON.md** | Guía completa | Antes de implementar |
| **ACLARACION_ARCHIVOS_HISTORICOS.md** | Evitar confusión | Si ves cr321_elemento1 |
| **RESUMEN_IMPLEMENTACION_COMPLETA.md** | Estado del proyecto | Referencia |

---

## ❓ Preguntas frecuentes

### ¿Necesito configurar Dataverse para probar?
❌ NO. Usa `python demo_local.py`

### ¿Necesito crear muchos campos en cr321_chatbots?
❌ NO. Solo 3 campos: cr321_config, cr321_active, cr321_name

### ¿Qué son cr321_elemento1, cr321_grupo1, cr321_orden?
⚠️ Son de análisis histórico. NO existen en la implementación actual.

### ¿Cómo agrego un nuevo menú?
✅ Edita JSON_LISTO_PARA_INSERTAR.json y ejecuta `python implementar_todo.py`

### ¿Funciona el sistema ya?
✅ SÍ. Ejecuta `python demo_local.py` para verlo

### ¿Puedo cambiar los grupos?
✅ SÍ. Solo actualiza los grupo_id en el JSON con GUIDs de tu tabla cr321_grupos

---

## 🆘 Si tienes problemas

### Error: "No se encuentra el archivo JSON"
```powershell
# Verifica que existe
dir JSON_LISTO_PARA_INSERTAR.json
```

### Error: "ModuleNotFoundError"
```powershell
pip install requests
```

### Confusión con campos cr321_elementoX
Lee: ACLARACION_ARCHIVOS_HISTORICOS.md

### Otro problema
1. Lee el mensaje de error completo
2. Verifica que estás usando archivos de "Implementación Actual"
3. NO uses archivos históricos (ANALISIS_, COMPARATIVA_, etc.)

---

## 🎉 ¡Listo!

Ya sabes todo lo que necesitas para empezar.

**Próximo paso:** Ejecuta `python demo_local.py` y ve el sistema funcionando.

**Después:** Lee README_INICIO_RAPIDO.md para entender cómo funciona.

**Por último:** Cuando estés listo, ejecuta `python implementar_todo.py` para subir a Dataverse.
