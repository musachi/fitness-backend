# Fitness Platform Backend

API RESTful para una aplicación de gimnasio construida con FastAPI y SQLAlchemy.

## 🚀 Características

- ✅ **FastAPI** - Framework moderno de alta performance
- ✅ **SQLAlchemy 2.0** - ORM con soporte async
- ✅ **PostgreSQL** - Base de datos robusta
- ✅ **Pydantic** - Validación de datos automática
- ✅ **Alembic** - Migraciones de base de datos
- ✅ **JWT** - Autenticación segura
- ✅ **Tests** - Suite completa de pruebas
- ✅ **Type Hints** - Código tipado estáticamente
- ✅ **OpenAPI** - Documentación automática

## 📋 Requisitos

- **Python 3.11+** (Recomendado: 3.11.9)
- **PostgreSQL 12+**
- **Poetry** (Para gestión de dependencias)

## 🛠️ Instalación

### Opción 1: Usando Poetry (Recomendado)

```bash
# Clonar el repositorio
git clone <repository-url>
cd fitness-backend

# Instalar Poetry (si no lo tienes)
pip install poetry

# Crear entorno virtual e instalar dependencias
poetry install

# Activar entorno virtual
poetry shell
```

### Opción 2: Usando pip y requirements.txt

```bash
# Asegurarse de tener Python 3.11+
python --version  # Debe ser 3.11.x

# Crear entorno virtual
python -m venv venv

# Activar entorno virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Instalar dependencias
pip install -r requirements.txt
```

## ⚙️ Configuración

### 1. Variables de Entorno

Copiar `.env.example` a `.env` y configurar:

```bash
cp .env.example .env
```

Variables requeridas:
```env
# Database
DATABASE_URL=postgresql://user:password@localhost:5432/fitness_db

# JWT
SECRET_KEY=your-secret-key-here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30

# API
PROJECT_NAME=Fitness Platform API
VERSION=1.0.0
DEBUG=False

# CORS (opcional)
BACKEND_CORS_ORIGINS=["http://localhost:3000"]
```

### 2. Base de Datos

```bash
# Crear base de datos PostgreSQL
createdb fitness_db

# Ejecutar migraciones
alembic upgrade head

# Opcional: Crear datos de prueba
python scripts/seed_data.py
```

## 🚀 Ejecución

### Desarrollo

```bash
# Usando Poetry
poetry run uvicorn src.main:app --reload --host 0.0.0.0 --port 8000

# Usando pip/venv
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

### Producción

```bash
# Sin recarga
uvicorn src.main:app --host 0.0.0.0 --port 8000 --workers 4

# O usando Gunicorn
gunicorn src.main:app -w 4 -k uvicorn.workers.UvicornWorker
```

## 📚 Documentación

Una vez iniciada la API:

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/api/v1/openapi.json

## 🧪 Testing

### Ejecutar todos los tests

```bash
# Usando Poetry
poetry run pytest

# Usando pip/venv
pytest
```

### Ejecutar tests específicos

```bash
# Tests de ejercicios
pytest tests/unit/test_exercise_endpoints.py -v

# Tests de CRUD
pytest tests/unit/test_exercise_crud.py -v

# Tests básicos de API
pytest tests/unit/test_basic_api.py -v

# Con coverage
pytest --cov=src tests/
```

### Tipos de Tests

- **Unit**: Tests de unidades individuales
- **Integration**: Tests de integración entre componentes
- **E2E**: Tests end-to-end

## 📁 Estructura del Proyecto

```
fitness-backend/
├── src/                          # Código fuente
│   ├── api/                       # Endpoints de la API
│   │   └── v1/
│   │       ├── endpoints/          # Endpoints específicos
│   │       └── router.py          # Router principal
│   ├── core/                      # Configuración central
│   ├── crud/                      # Operaciones CRUD
│   ├── models/                    # Modelos de base de datos
│   ├── schemas/                   # Schemas Pydantic
│   └── utils/                     # Utilidades varias
├── tests/                         # Tests
│   ├── unit/                     # Tests unitarios
│   ├── integration/               # Tests de integración
│   └── conftest.py               # Configuración de tests
├── alembic/                      # Migraciones
├── docs/                         # Documentación
├── scripts/                      # Scripts varios
├── pyproject.toml               # Configuración de Poetry
├── requirements.txt             # Dependencias (alternativa)
└── .env.example                  # Variables de entorno ejemplo
```

## 🔧 Endpoints Principales

### Ejercicios
- `GET /api/v1/exercises/` - Listar ejercicios
- `POST /api/v1/exercises/` - Crear ejercicio
- `GET /api/v1/exercises/{id}` - Obtener ejercicio
- `PUT /api/v1/exercises/{id}` - Actualizar ejercicio
- `DELETE /api/v1/exercises/{id}` - Eliminar ejercicio

### Clasificaciones
- `GET /api/v1/exercises/categories/` - Categorías
- `GET /api/v1/exercises/movement-types/` - Tipos de movimiento
- `GET /api/v1/exercises/muscle-groups/` - Grupos musculares
- `GET /api/v1/exercises/equipment/` - Equipos
- `GET /api/v1/exercises/positions/` - Posiciones
- `GET /api/v1/exercises/contraction-types/` - Tipos de contracción

### Usuarios
- `POST /api/v1/auth/login` - Login
- `POST /api/v1/auth/register` - Registro
- `GET /api/v1/users/me` - Perfil del usuario actual

## 🏋‍♂️ Modelo de Datos

La aplicación incluye modelos para:

- **Usuarios**: Roles, perfiles, autenticación
- **Ejercicios**: Ejercicios con todas sus clasificaciones
- **Planes**: Planes de entrenamiento
- **Sesiones**: Sesiones de workout
- **Progreso**: Seguimiento del progreso

## 🔒 Seguridad

- ✅ Autenticación JWT
- ✅ Hashing de contraseñas (bcrypt)
- ✅ Validación de datos (Pydantic)
- ✅ CORS configurado
- ✅ Rate limiting (por implementar)
- ✅ Input sanitization

## 🚀 Despliegue

### Docker

```bash
# Construir imagen
docker build -t fitness-api .

# Ejecutar contenedor
docker run -p 8000:8000 fitness-api
```

### Docker Compose

```bash
# Iniciar todos los servicios
docker-compose up -d

# Ver logs
docker-compose logs -f

# Detener servicios
docker-compose down
```

## 📈 Monitoring

La aplicación incluye:

- **Logging** con Loguru
- **Health checks** en `/api/v1/health`
- **OpenAPI** para documentación automática
- **Metrics** (por implementar con Prometheus)

## 🤝 Contribución

1. Fork del proyecto
2. Crear feature branch (`git checkout -b feature/amazing-feature`)
3. Commit cambios (`git commit -m 'Add amazing feature'`)
4. Push al branch (`git push origin feature/amazing-feature`)
5. Abrir Pull Request

## 📝 Licencia

Este proyecto está bajo licencia MIT. Ver archivo LICENSE para detalles.

## 🆘️ Soporte

Para soporte o preguntas:

- Crear un issue en GitHub
- Email: adonys.cu2012@gmail.com
- Documentación: Ver carpeta `docs/`

---

**Nota**: Esta API está diseñada para ser el backend de una aplicación móvil/web de fitness. Proporciona todos los endpoints necesarios para gestionar ejercicios, planes de entrenamiento, seguimiento de progreso y gestión de usuarios.
