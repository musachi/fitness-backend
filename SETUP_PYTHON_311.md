# 🐍 Configuración de Python 3.11 - Guía de Instalación

## Problema Actual
Estás usando Python 3.14.2, pero SQLAlchemy 2.0.23 no es compatible con esta versión. Necesitamos usar Python 3.11.

## 🔧 Solución

### Opción 1: Instalar Python 3.11 (Recomendado)

#### Windows:
1. **Descargar Python 3.11** desde https://www.python.org/downloads/release/python-3119/
2. **Desinstalar Python 3.14** (si es necesario)
3. **Instalar Python 3.11.9** marcando "Add to PATH"
4. **Verificar instalación**:
```bash
python --version  # Debe mostrar Python 3.11.9
```

#### Usar pyenv (Alternativa):
```bash
# Instalar pyenv
pip install pyenv-win

# Instalar Python 3.11.9
pyenv install 3.11.9
pyenv local 3.11.9

# Verificar
python --version
```

### Opción 2: Actualizar SQLAlchemy (Temporal)

Podemos actualizar a una versión compatible con Python 3.14:

```bash
pip install --upgrade sqlalchemy
pip install "sqlalchemy>=2.0.25"
```

## 🚀 Pasos para Configurar el Entorno

### 1. Verificar Versión de Python
```bash
python --version
# Debe ser: Python 3.11.x
```

### 2. Limpiar Entorno Virtual Actual
```bash
# Si existe un venv, eliminarlo
rmdir /s venv

# Crear nuevo entorno virtual con Python 3.11
python -m venv venv
```

### 3. Activar Entorno Virtual
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

### 4. Instalar Dependencias
```bash
# Usar requirements.txt
pip install -r requirements.txt

# O usar Poetry
poetry install
```

### 5. Verificar Instalación
```bash
# Verificar que todo esté instalado correctamente
python -c "import sqlalchemy; print('SQLAlchemy version:', sqlalchemy.__version__)"

# Probar imports principales
python -c "from src.main import app; print('App imported successfully')"
```

## 🧪 Ejecutar Tests

Una vez configurado Python 3.11:

```bash
# Ejecutar tests básicos
python -m pytest tests/unit/test_basic_api.py -v

# Ejecutar todos los tests
python -m pytest tests/ -v

# Con coverage
python -m pytest --cov=src tests/ -v
```

## 📋 Checklist de Verificación

- [ ] Python 3.11.9 instalado
- [ ] Entorno virtual creado con Python 3.11
- [ ] Dependencias instaladas sin errores
- [ ] Tests ejecutan sin ImportError
- [ ] API inicia correctamente
- [ ] Documentación accesible en http://localhost:8000/docs

## 🚨 Si Siguen Habiendo Problemas

### Opción A: Usar Docker
```bash
# Construir con Python 3.11
docker build -t fitness-api .

# Ejecutar
docker run -p 8000:8000 fitness-api
```

### Opción B: Downgrade Gradual
```bash
# Instalar versiones compatibles
pip install sqlalchemy==2.0.23
pip install fastapi==0.104.1
pip install pydantic==2.5.0
```

## 🔄 Comandos Útiles

```bash
# Verificar versión de Python
python --version

# Verificar versión de paquetes
pip list | findstr sqlalchemy
pip list | findstr fastapi

# Forzar reinstalación
pip uninstall sqlalchemy
pip install sqlalchemy==2.0.23

# Verificar PATH
where python
```

## 📝 Notas Importantes

1. **Python 3.11 es la versión recomendada** para estabilidad
2. **SQLAlchemy 2.0.23** es estable y probada con Python 3.11
3. **FastAPI 0.104.1** funciona perfectamente con Python 3.11
4. **Poetry** automáticamente usará la versión correcta si está en .python-version

## 🎯 Prueba Rápida

Después de configurar Python 3.11, ejecuta:

```bash
python -c "
import sys
print(f'Python version: {sys.version}')
import sqlalchemy
print(f'SQLAlchemy version: {sqlalchemy.__version__}')
import fastapi
print(f'FastAPI version: {fastapi.__version__}')
print('✅ Todo configurado correctamente!')
"
```

Si ves el mensaje "✅ Todo configurado correctamente!", estás listo para continuar!
