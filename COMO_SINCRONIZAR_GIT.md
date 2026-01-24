# 📘 Guía: Cómo Sincronizar con GitHub

## 🔄 Flujo completo de sincronización

### 1️⃣ Ver qué archivos cambiaron
```powershell
git status
```
**Salida ejemplo:**
```
Changes not staged for commit:
  modified:   README.md
  deleted:    api_endpoints.py

Untracked files:
  cambiar_entorno.ps1
  mobile/config.py
```

---

### 2️⃣ Agregar archivos al stage (preparar cambios)
```powershell
# Agregar TODO (recomendado)
git add -A

# O agregar archivos específicos
git add README.md
git add mobile/config.py
```

**¿Qué hace `git add`?**
- Marca archivos para incluir en el próximo commit
- `-A` = Agrega TODO (nuevos, modificados, eliminados)

---

### 3️⃣ Hacer commit (guardar en Git local)
```powershell
git commit -m "Descripción de los cambios"
```

**Ejemplo:**
```powershell
git commit -m "feat: Agregar configuración de entornos LOCAL/AZURE"
```

**¿Qué hace `git commit`?**
- Guarda los cambios en tu repositorio LOCAL
- `-m` = Mensaje describiendo qué cambiaste
- **Todavía NO se sube a GitHub**

---

### 4️⃣ Subir a GitHub (sincronizar)
```powershell
git push origin main
```

**¿Qué hace `git push`?**
- Sube tus commits locales a GitHub
- `origin` = nombre del repositorio remoto (GitHub)
- `main` = rama principal

---

## 🚀 Atajo: Todo en una secuencia
```powershell
git add -A
git commit -m "Descripción de cambios"
git push origin main
```

---

## 📊 Estados de Git

| Comando | Estado | ¿En GitHub? |
|---------|--------|-------------|
| **Editas archivo** | Workspace (modified) | ❌ NO |
| `git add` | Staged | ❌ NO |
| `git commit` | Local Repository | ❌ NO |
| `git push` | Remote (GitHub) | ✅ SÍ |

---

## ⚠️ Errores Comunes

### Error 1: Olvidar `git add`
```powershell
git status  # muestra archivos modificados
git commit -m "Cambios"  # ❌ No incluye los archivos
```
**Solución:** Hacer `git add -A` primero

### Error 2: Olvidar `git push`
```powershell
git commit -m "Cambios"  # ✅ Guardado LOCAL
# ... cierras la terminal ...
# GitHub sigue sin tus cambios ❌
```
**Solución:** Siempre hacer `git push` después del commit

### Error 3: No revisar qué se sube
```powershell
git add -A  # Incluye TODO (¡cuidado con archivos sensibles!)
```
**Solución:** Usar `.gitignore` para excluir archivos

---

## 🔍 Comandos útiles

### Ver historial de commits
```powershell
git log --oneline
```

### Ver diferencias (qué cambió)
```powershell
git diff README.md
```

### Deshacer cambios no commiteados
```powershell
git restore README.md  # Descartar cambios de un archivo
git restore .          # Descartar TODOS los cambios
```

### Ver archivos en stage
```powershell
git diff --cached
```

---

## 📝 Workflow Recomendado

```powershell
# 1. Antes de trabajar: traer cambios de GitHub
git pull origin main

# 2. Hacer tus cambios en archivos...

# 3. Revisar qué cambió
git status

# 4. Preparar y subir
git add -A
git commit -m "feat: Descripción clara de cambios"
git push origin main

# 5. Verificar en GitHub que se subió
```

---

## 🎯 Ejemplo Real (lo que hicimos hoy)

```powershell
PS C:\VS\CLAUDE-1> git status
# Vimos: archivos modificados, eliminados, sin seguimiento

PS C:\VS\CLAUDE-1> git add -A
# Agregamos TODO al stage

PS C:\VS\CLAUDE-1> git commit -m "feat: Consolidar backend..."
# Guardamos en Git local
# [main 459c372] feat: Consolidar backend...

PS C:\VS\CLAUDE-1> git push origin main
# Subimos a GitHub
# Enumerating objects: 25, done.
# Writing objects: 100% (15/15), 5.16 KiB
# To https://github.com/SBApoyo/WP0.git
#    e9c6103..459c372  main -> main
```

✅ **Ahora GitHub tiene todos tus cambios**

---

## 📌 Resumen

| Para... | Comando |
|---------|---------|
| Ver estado | `git status` |
| Preparar cambios | `git add -A` |
| Guardar local | `git commit -m "mensaje"` |
| Subir a GitHub | `git push origin main` |
| Bajar de GitHub | `git pull origin main` |

**Regla de oro:** 
```
git add → git commit → git push
```
¡En ese orden! 🎯
