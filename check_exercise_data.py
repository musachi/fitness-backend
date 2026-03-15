from src.core.database import get_db
from src.models.exercise import Exercise
db = next(get_db())

print('🔍 Verificando ejercicios y sus clasificaciones:')
print('=' * 60)

exercises = db.query(Exercise).all()
for ex in exercises:
    print(f'\n📋 Ejercicio: {ex.name} (ID: {ex.id})')
    print(f'📊 Clasificaciones: {len(ex.classification_values)}')
    
    if ex.classification_values:
        for cv in ex.classification_values:
            print(f'  • {cv.classification_type.name}: {cv.value}')
    else:
        print('  ❌ No tiene clasificaciones')
        
    # Verificar si tiene propiedades hardcodeadas
    print(f'🔍 Propiedades hardcodeadas:')
    print(f'  • movement_type: {getattr(ex, "movement_type_id", "No existe")}')
    print(f'  • muscle_group: {getattr(ex, "muscle_group_id", "No existe")}')
    print(f'  • equipment: {getattr(ex, "equipment_id", "No existe")}')
