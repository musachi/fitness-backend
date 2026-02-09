# API de Ejercicios - Documentación

## Overview

Esta documentación describe todos los endpoints disponibles para la gestión de ejercicios y sus clasificaciones en la API del gimnasio.

## Autenticación

La mayoría de los endpoints requieren autenticación. Los usuarios con rol de "Coach" o "Admin" pueden crear, actualizar y eliminar ejercicios y clasificaciones.

## Endpoints de Ejercicios

### GET /api/v1/exercises/
Obtener lista de ejercicios con filtros opcionales.

**Query Parameters:**
- `skip` (int, optional): Número de registros a saltar (default: 0)
- `limit` (int, optional): Número máximo de registros a devolver (default: 100, max: 1000)
- `coach_id` (UUID, optional): Filtrar por coach
- `category_id` (int, optional): Filtrar por categoría
- `muscle_group_id` (int, optional): Filtrar por grupo muscular
- `equipment_id` (int, optional): Filtrar por equipo
- `search` (string, optional): Buscar por nombre o descripción

**Response:**
```json
{
  "exercises": [
    {
      "id": 1,
      "name": "Bench Press",
      "short_name": "BP",
      "description": "Classic chest exercise",
      "coach_id": "uuid",
      "category_id": 1,
      "movement_type_id": 1,
      "muscle_group_id": 1,
      "equipment_id": 1,
      "position_id": 1,
      "contraction_type_id": 1,
      "type": "strength",
      "crossfit_variant": null,
      "created_at": "2024-01-01T00:00:00",
      "updated_at": "2024-01-01T00:00:00",
      "category": {"id": 1, "name": "Strength"},
      "movement_type": {"id": 1, "name": "Compound"},
      "muscle_group": {"id": 1, "name": "Chest"},
      "equipment": {"id": 1, "name": "Barbell"},
      "position": {"id": 1, "name": "Standing"},
      "contraction_type": {"id": 1, "name": "Concentric"}
    }
  ],
  "total": 1,
  "page": 1,
  "size": 100
}
```

### GET /api/v1/exercises/{exercise_id}
Obtener un ejercicio específico por ID.

### POST /api/v1/exercises/
Crear un nuevo ejercicio (requiere autenticación de coach).

**Request Body:**
```json
{
  "name": "New Exercise",
  "short_name": "NE",
  "description": "Exercise description",
  "category_id": 1,
  "movement_type_id": 1,
  "muscle_group_id": 1,
  "equipment_id": 1,
  "position_id": 1,
  "contraction_type_id": 1,
  "type": "strength",
  "crossfit_variant": {"rounds": 3, "reps": 10}
}
```

### PUT /api/v1/exercises/{exercise_id}
Actualizar un ejercicio existente (solo creador o admin).

### DELETE /api/v1/exercises/{exercise_id}
Eliminar un ejercicio (solo creador o admin).

### GET /api/v1/exercises/coach/mine
Obtener ejercicios creados por el coach actual.

## Endpoints de Clasificaciones

### Categorías de Ejercicios

#### GET /api/v1/exercises/categories/
Obtener todas las categorías de ejercicios.

**Response:**
```json
{
  "categories": [
    {
      "id": 1,
      "name": "Strength",
      "displacement": false,
      "metabolic_type": "anaerobic"
    }
  ],
  "total": 1
}
```

#### GET /api/v1/exercises/categories/{category_id}
Obtener una categoría específica.

#### POST /api/v1/exercises/categories/
Crear una nueva categoría (requiere autenticación).

**Request Body:**
```json
{
  "name": "Cardio",
  "displacement": true,
  "metabolic_type": "aerobic"
}
```

#### PUT /api/v1/exercises/categories/{category_id}
Actualizar una categoría existente.

#### DELETE /api/v1/exercises/categories/{category_id}
Eliminar una categoría existente.

### Tipos de Movimiento

#### GET /api/v1/exercises/movement-types/
Obtener todos los tipos de movimiento.

#### GET /api/v1/exercises/movement-types/{movement_type_id}
Obtener un tipo de movimiento específico.

#### POST /api/v1/exercises/movement-types/
Crear un nuevo tipo de movimiento (requiere autenticación).

**Request Body:**
```json
{
  "name": "Compound"
}
```

#### PUT /api/v1/exercises/movement-types/{movement_type_id}
Actualizar un tipo de movimiento existente.

#### DELETE /api/v1/exercises/movement-types/{movement_type_id}
Eliminar un tipo de movimiento existente.

### Grupos Musculares

#### GET /api/v1/exercises/muscle-groups/
Obtener todos los grupos musculares.

#### GET /api/v1/exercises/muscle-groups/{muscle_group_id}
Obtener un grupo muscular específico.

#### POST /api/v1/exercises/muscle-groups/
Crear un nuevo grupo muscular (requiere autenticación).

**Request Body:**
```json
{
  "name": "Chest"
}
```

#### PUT /api/v1/exercises/muscle-groups/{muscle_group_id}
Actualizar un grupo muscular existente.

#### DELETE /api/v1/exercises/muscle-groups/{muscle_group_id}
Eliminar un grupo muscular existente.

### Equipos

#### GET /api/v1/exercises/equipment/
Obtener todos los equipos.

#### GET /api/v1/exercises/equipment/{equipment_id}
Obtener un equipo específico.

#### POST /api/v1/exercises/equipment/
Crear un nuevo equipo (requiere autenticación).

**Request Body:**
```json
{
  "name": "Barbell"
}
```

#### PUT /api/v1/exercises/equipment/{equipment_id}
Actualizar un equipo existente.

#### DELETE /api/v1/exercises/equipment/{equipment_id}
Eliminar un equipo existente.

### Posiciones

#### GET /api/v1/exercises/positions/
Obtener todas las posiciones.

#### GET /api/v1/exercises/positions/{position_id}
Obtener una posición específica.

#### POST /api/v1/exercises/positions/
Crear una nueva posición (requiere autenticación).

**Request Body:**
```json
{
  "name": "Standing"
}
```

#### PUT /api/v1/exercises/positions/{position_id}
Actualizar una posición existente.

#### DELETE /api/v1/exercises/positions/{position_id}
Eliminar una posición existente.

### Tipos de Contracción

#### GET /api/v1/exercises/contraction-types/
Obtener todos los tipos de contracción.

#### GET /api/v1/exercises/contraction-types/{contraction_type_id}
Obtener un tipo de contracción específico.

#### POST /api/v1/exercises/contraction-types/
Crear un nuevo tipo de contracción (requiere autenticación).

**Request Body:**
```json
{
  "name": "Concentric"
}
```

#### PUT /api/v1/exercises/contraction-types/{contraction_type_id}
Actualizar un tipo de contracción existente.

#### DELETE /api/v1/exercises/contraction-types/{contraction_type_id}
Eliminar un tipo de contracción existente.

## Ejemplos de Uso

### Crear un Ejercicio Completo

```bash
curl -X POST "http://localhost:8000/api/v1/exercises/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Squat",
    "short_name": "SQ",
    "description": "Basic leg exercise",
    "category_id": 1,
    "movement_type_id": 1,
    "muscle_group_id": 2,
    "equipment_id": 1,
    "position_id": 2,
    "contraction_type_id": 1,
    "type": "strength"
  }'
```

### Buscar Ejercicios

```bash
curl "http://localhost:8000/api/v1/exercises/?search=Squat&limit=10"
```

### Filtrar por Categoría

```bash
curl "http://localhost:8000/api/v1/exercises/?category_id=1"
```

### Crear Nueva Categoría

```bash
curl -X POST "http://localhost:8000/api/v1/exercises/categories/" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Flexibility",
    "displacement": true,
    "metabolic_type": "aerobic"
  }'
```

## Códigos de Estado

- `200 OK`: Solicitud exitosa
- `201 Created`: Recurso creado exitosamente
- `204 No Content`: Recurso eliminado exitosamente
- `400 Bad Request`: Datos inválidos o duplicados
- `401 Unauthorized`: Requiere autenticación
- `403 Forbidden`: Permisos insuficientes
- `404 Not Found`: Recurso no encontrado
- `422 Unprocessable Entity`: Error de validación

## Consideraciones

1. **Permisos**: Solo coaches y admins pueden crear/actualizar/eliminar ejercicios y clasificaciones
2. **Validación**: Se valida que no existan nombres duplicados en clasificaciones
3. **Relaciones**: Los endpoints de ejercicios devuelven las relaciones cargadas para mejor UX
4. **Paginación**: Todos los endpoints de lista soportan paginación con `skip` y `limit`
5. **Búsqueda**: Los ejercicios soportan búsqueda por nombre, short_name y descripción
