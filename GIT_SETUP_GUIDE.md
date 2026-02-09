# 🚀 **Guía Git: Configuración de Repositorio y Branch Strategy**

## ✅ **Estado Actual del Repositorio**

- ✅ **Repositorio Git inicializado** (local)
- ✅ **Branch actual:** `master`
- ❌ **Sin commits** aún
- ❌ **Sin remotes** configurados
- ✅ **.gitignore configurado**

## 🌟 **Estrategia de Branches Recomendada**

```
master      ←─── Producción (solo releases estables)
develop     ←─── Desarrollo integrado
production  ←─── Producción actual (si necesitas separar)
```

## 📋 **Pasos para Configurar el Repositorio**

### **Paso 1: Configurar Usuario Git (si no lo has hecho)**
```bash
git config --global user.name "Tu Nombre"
git config --global user.email "tu.email@example.com"
```

### **Paso 2: Crear los Branches Principales**
```bash
# Crear branch develop desde master
git checkout -b develop

# Crear branch production desde master
git checkout -b production

# Volver a master
git checkout master
```

### **Paso 3: Hacer el Primer Commit (Initial Setup)**
```bash
# Agregar todos los archivos
git add .

# Hacer commit inicial
git commit -m "🎉 Initial commit: FastAPI fitness backend

- ✅ Complete CRUD operations for exercises and classifications
- ✅ API endpoints with authentication and validation
- ✅ Comprehensive test suite (15 tests passing)
- ✅ Python 3.14 compatibility
- ✅ Documentation and setup guides
- ✅ Database models and schemas
- ✅ Pydantic validation and FastAPI routing

Features:
- Exercise management (CRUD, search, filtering)
- Classification management (categories, movement types, muscle groups, equipment, positions, contraction types)
- Coach authentication and authorization
- Pagination and filtering
- OpenAPI documentation
- Test coverage for all endpoints"
```

### **Paso 4: Configurar Remote (conectar a GitHub/GitLab/etc.)**

#### **Opción A: Crear Nuevo Repositorio**
```bash
# Agregar remote (reemplaza URL con tu repo)
git remote add origin https://github.com/tu-usuario/fitness-backend.git

# Push branches al remote
git push -u origin master
git push -u origin develop
git push -u origin production
```

#### **Opción B: Conectar a Repositorio Existente**
```bash
# Si el repo ya existe y tiene los 3 branches
git remote add origin https://github.com/tu-usuario/fitness-backend.git

# Fetch branches del remote
git fetch origin

# Configurar upstream para cada branch
git branch --set-upstream-to=origin/master master
git branch --set-upstream-to=origin/develop develop
git branch --set-upstream-to=origin/production production

# Push cambios locales
git push origin master
git push origin develop
git push origin production
```

### **Paso 5: Configurar Branch Strategy**

```bash
# Configurar master como branch principal
git checkout master
git branch --set-upstream-to=origin/master master

# Configurar develop para desarrollo
git checkout develop
git branch --set-upstream-to=origin/develop develop

# Configurar production para producción
git checkout production
git branch --set-upstream-to=origin/production production
```

## 🔄 **Flujo de Trabajo Recomendado**

### **Desarrollo Normal:**
```bash
# 1. Trabajar en develop
git checkout develop
git pull origin develop

# 2. Crear feature branch
git checkout -b feature/nueva-funcionalidad

# 3. Hacer cambios y commits
git add .
git commit -m "✨ feat: add new exercise filtering"

# 4. Merge a develop
git checkout develop
git merge feature/nueva-funcionalidad
git push origin develop

# 5. Eliminar feature branch
git branch -d feature/nueva-funcionalidad
```

### **Release a Producción:**
```bash
# 1. Desde develop crear release
git checkout develop
git pull origin develop
git checkout -b release/v1.0.0

# 2. Merge a master
git checkout master
git merge release/v1.0.0
git tag v1.0.0
git push origin master
git push origin v1.0.0

# 3. Merge a production
git checkout production
git merge master
git push origin production

# 4. Merge de vuelta a develop
git checkout develop
git merge master
git push origin develop
```

## 🛡️ **Protección de Branches (Recomendado)**

### **En GitHub/GitLab:**
- **master:** Proteger, requerir PR y aprobaciones
- **develop:** Proteger, requerir PR
- **production:** Proteger, solo merges desde master

## 📝 **Comandos Útiles**

```bash
# Ver todos los branches
git branch -a

# Ver estado actual
git status

# Ver commits
git log --oneline --graph --all

# Ver remotes
git remote -v

# Cambiar entre branches
git checkout master
git checkout develop
git checkout production

# Ver diferencias
git diff master..develop
git diff develop..production
```

## 🚨 **Buenas Prácticas**

1. **Nunca trabajar directamente en master**
2. **Siempre crear feature branches desde develop**
3. **Usar commits descriptivos con emojis**
4. **Hacer pull antes de push**
5. **Escribir tests para nuevas funcionalidades**
6. **Documentar cambios importantes**

## 🎯 **Estado Final Esperado**

```bash
git branch -a
* master
  develop
  production
  remotes/origin/master
  remotes/origin/develop
  remotes/origin/production
```

## 📋 **Checklist de Verificación**

- [ ] Usuario Git configurado
- [ ] .gitignore completo
- [ ] Branches creados (master, develop, production)
- [ ] Primer commit realizado
- [ ] Remote configurado
- [ ] Branches push al remote
- [ ] Protección de branches configurada
- [ ] Flujo de trabajo definido

**🎉 ¡Repositorio listo para desarrollo en equipo!**
