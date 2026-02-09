import os
import sys
import uuid

from sqlalchemy.orm import Session

from src.core.database import SessionLocal
from src.crud import exercise, exercise_category, role, user
from src.schemas.exercise import ExerciseCategoryCreate, ExerciseCreate
from src.schemas.user import RoleCreate, UserCreate

sys.path.append(os.path.join(os.path.dirname(__file__), "src"))


def test_crud_operations():
    """Test basic CRUD operations with unique data"""
    db: Session = SessionLocal()

    try:
        print("🧪 Probando operaciones CRUD...")

        # Generar datos únicos para esta prueba
        test_suffix = uuid.uuid4().hex[:8]

        # 1. Test Role CRUD
        print("\n1. Probando Role CRUD...")  # TODO change to Role create
        role_data = RoleCreate(
            name=f"test_role_{test_suffix}",
            description="Test role for testing",  # TODO add more fields if needed, change description
            is_paid=False,
        )

        created_role = role.create(db, obj_in=role_data)
        print(f"✅ Role creado: {created_role.name} (ID: {created_role.id})")

        # 2. Test User CRUD
        print("\n2. Probando User CRUD...")
        user_data = UserCreate(
            name="Test User",
            email=f"test_{test_suffix}@example.com",
            password="test123",  # Password corta para bcrypt
            role_id=created_role.id,
        )

        created_user = user.create(db, obj_in=user_data)
        print(f"✅ Usuario creado: {created_user.name} (ID: {created_user.id})")

        # 3. Test Get operations
        print("\n3. Probando operaciones GET...")

        # Get user by email
        found_user = user.get_by_email(db, email=user_data.email)
        print(
            f"✅ Usuario encontrado por email: {found_user.email if found_user else 'No encontrado'}"
        )

        # Get role by name
        found_role = role.get_by_name(db, name=role_data.name)
        print(
            f"✅ Role encontrado por nombre: {found_role.name if found_role else 'No encontrado'}"
        )

        # 4. Test Exercise Category CRUD
        print("\n4. Probando Exercise Category CRUD...")
        category_data = ExerciseCategoryCreate(
            name=f"Test Category {test_suffix}",
            displacement=False,
            metabolic_type="strength",
        )

        created_category = exercise_category.create(db, obj_in=category_data)
        print(
            f"✅ Categoría creada: {created_category.name} (ID: {created_category.id})"
        )

        # 5. Test Exercise CRUD
        print("\n5. Probando Exercise CRUD...")
        exercise_data = ExerciseCreate(
            name=f"Test Exercise {test_suffix}",
            short_name=f"TestEx_{test_suffix[:4]}",
            description="Test exercise for testing",
            category_id=created_category.id,
        )

        created_exercise = exercise.create(db, obj_in=exercise_data)
        print(
            f"✅ Ejercicio creado: {created_exercise.name} (ID: {created_exercise.id})"
        )

        # 6. Test List operations
        print("\n6. Probando operaciones de lista...")

        # List users
        users = user.get_multi(db, skip=0, limit=5)
        print(f"✅ Usuarios totales: {len(users)}")

        # List exercises
        exercises = exercise.get_multi(db, skip=0, limit=5)
        print(f"✅ Ejercicios totales: {len(exercises)}")

        # List categories
        categories = exercise_category.get_multi(db, skip=0, limit=5)
        print(f"✅ Categorías totales: {len(categories)}")

        print("\n🎉 ¡Todas las pruebas CRUD pasaron exitosamente!")

        # Cleanup (opcional)
        db.rollback()  # No guardamos los cambios de prueba
        print("\n🧹 Cambios revertidos (solo prueba)")

    except Exception as e:
        print(f"❌ Error en pruebas CRUD: {e}")
        import traceback

        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    test_crud_operations()
