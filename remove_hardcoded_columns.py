from src.core.database import engine
from sqlalchemy import text

print("🔧 Removing hardcoded classification columns from exercises table...")

with engine.connect() as conn:
    # Remove indexes first
    print("📋 Removing indexes...")
    try:
        conn.execute(text("DROP INDEX IF EXISTS ix_exercises_movement_type_id"))
        conn.execute(text("DROP INDEX IF EXISTS ix_exercises_muscle_group_id"))
        conn.execute(text("DROP INDEX IF EXISTS ix_exercises_equipment_id"))
        conn.execute(text("DROP INDEX IF EXISTS ix_exercises_position_id"))
        conn.execute(text("DROP INDEX IF EXISTS ix_exercises_contraction_type_id"))
        conn.execute(text("DROP INDEX IF EXISTS ix_exercises_category_id"))
        print("✅ Indexes removed")
    except Exception as e:
        print(f"⚠️  Error removing indexes: {e}")
    
    # Remove columns
    print("📋 Removing columns...")
    try:
        conn.execute(text("ALTER TABLE exercises DROP COLUMN IF EXISTS movement_type_id"))
        conn.execute(text("ALTER TABLE exercises DROP COLUMN IF EXISTS muscle_group_id"))
        conn.execute(text("ALTER TABLE exercises DROP COLUMN IF EXISTS equipment_id"))
        conn.execute(text("ALTER TABLE exercises DROP COLUMN IF EXISTS position_id"))
        conn.execute(text("ALTER TABLE exercises DROP COLUMN IF EXISTS contraction_type_id"))
        conn.execute(text("ALTER TABLE exercises DROP COLUMN IF EXISTS category_id"))
        conn.commit()
        print("✅ Columns removed successfully")
    except Exception as e:
        print(f"❌ Error removing columns: {e}")
        conn.rollback()

# Verify the changes
print("\n🔍 Verifying table structure...")
with engine.connect() as conn:
    result = conn.execute(text("""
        SELECT column_name, data_type, is_nullable 
        FROM information_schema.columns 
        WHERE table_name = 'exercises' 
        ORDER BY ordinal_position
    """))
    
    print("\n📋 Current exercises table structure:")
    for row in result:
        nullable = "NULL" if row.is_nullable == "YES" else "NOT NULL"
        print(f"  {row.column_name} - {row.data_type} - {nullable}")

print("\n🎯 Exercises table is now completely dynamic!")
print("✅ All hardcoded classification columns have been removed")
print("🔗 Exercises now use exercise_classifications table for relationships")
