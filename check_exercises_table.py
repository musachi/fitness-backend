from src.core.database import engine
from sqlalchemy import inspect, text

inspector = inspect(engine)
exercises_table = inspector.get_columns('exercises')

print('🏗️  ESTRUCTURA ACTUAL DE LA TABLA EXERCISES:')
print('=' * 60)

for col in exercises_table:
    nullable = 'NULL' if col['nullable'] else 'NOT NULL'
    default = f" DEFAULT {col['default']}" if col['default'] else ''
    print(f'📋 {col["name"]} - {col["type"]} - {nullable} {default}')

print()
print('🎯 COLUMNAS HARDCODEADAS QUE DEBERÍAN ELIMINARSE:')
hardcoded_columns = ['movement_type_id', 'muscle_group_id', 'equipment_id', 'goal_id', 'exercise_category_id']
for col in exercises_table:
    if col['name'] in hardcoded_columns:
        print(f'❌ {col["name"]} - DEBERÍA ELIMINARSE')
        
print()
print('✅ COLUMNAS CORRECTAS QUE DEBEN MANTENERSE:')
correct_columns = ['id', 'name', 'short_name', 'description', 'coach_id', 'is_active', 'created_at', 'updated_at']
for col in exercises_table:
    if col['name'] in correct_columns:
        print(f'✅ {col["name"]} - CORRECTA')
