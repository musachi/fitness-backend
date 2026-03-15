from src.core.database import get_db
from src.models.exercise import Exercise
db = next(get_db())

print('🔍 Lista de todos los ejercicios en la base de datos:')
print('=' * 60)

exercises = db.query(Exercise).all()
for ex in exercises:
    print(f'📋 ID: {ex.id} | Nombre: "{ex.name}"')
    print(f'   📊 Clasificaciones: {len(ex.classification_values)}')
    if ex.classification_values:
        for cv in ex.classification_values:
            print(f'     • {cv.classification_type.name}: {cv.value}')
    print()

print(f'📈 Total ejercicios: {len(exercises)}')
