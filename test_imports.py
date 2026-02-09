import os
import sys

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))

try:
    # Probar imports
    from src.core.config import settings
    from src.schemas import ExerciseCreate, UserCreate

    print("✅ Todos los imports funcionan correctamente!")
    print(f"📁 Database URL: {settings.DATABASE_URL}")
    print(f"🔐 Secret Key configurado: {'Sí' if settings.SECRET_KEY else 'No'}")

    # Probar creación de schemas
    user_data = {
        "name": "Test User",
        "email": "test@example.com",
        "password": "password123",
        "role_id": 1,
    }

    exercise_data = {
        "name": "Push Up",
        "short_name": "PushUp",
        "description": "Standard push up",
    }

    user_schema = UserCreate(**user_data)
    exercise_schema = ExerciseCreate(**exercise_data)

    print(f"✅ Schema User válido: {user_schema.email}")
    print(f"✅ Schema Exercise válido: {exercise_schema.name}")

except Exception as e:
    print(f"❌ Error en imports: {e}")
    import traceback

    traceback.print_exc()
