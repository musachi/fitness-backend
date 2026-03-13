#!/usr/bin/env python3
"""
Check and create classification data if needed
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from src.core.database import SessionLocal

def check_and_create_classifications():
    db = SessionLocal()
    try:
        print("=== CHECKING CLASSIFICATION TYPES ===")
        result = db.execute(text("SELECT COUNT(*) FROM classification_types"))
        type_count = result.scalar()
        print(f"Classification types count: {type_count}")
        
        if type_count == 0:
            print("Creating classification types...")
            # Create classification types
            db.execute(text("""
                INSERT INTO classification_types (name, description, applies_to, is_required, created_at, updated_at) VALUES
                ('Movement Type', 'Type of movement for exercises', 'exercises', false, NOW(), NOW()),
                ('Muscle Group', 'Primary muscle group targeted', 'exercises', false, NOW(), NOW()),
                ('Equipment', 'Equipment needed for the exercise', 'exercises', false, NOW(), NOW()),
                ('Position', 'Body position during exercise', 'exercises', false, NOW(), NOW()),
                ('Contraction Type', 'Type of muscle contraction', 'exercises', false, NOW(), NOW())
            """))
            db.commit()
            print("Created classification types")
        
        print("\n=== CHECKING CLASSIFICATION VALUES ===")
        result = db.execute(text("SELECT COUNT(*) FROM classification_values"))
        value_count = result.scalar()
        print(f"Classification values count: {value_count}")
        
        if value_count == 0:
            print("Creating classification values...")
            # Get the type IDs we just created
            result = db.execute(text("SELECT id, name FROM classification_types ORDER BY id"))
            types = {row[1]: row[0] for row in result}
            
            # Create values for each type
            values_data = [
                # Movement Types
                (types['Movement Type'], 'Compound'),
                (types['Movement Type'], 'Isolation'),
                
                # Muscle Groups
                (types['Muscle Group'], 'Chest'),
                (types['Muscle Group'], 'Back'),
                (types['Muscle Group'], 'Legs'),
                (types['Muscle Group'], 'Shoulders'),
                (types['Muscle Group'], 'Arms'),
                (types['Muscle Group'], 'Core'),
                
                # Equipment
                (types['Equipment'], 'Barbell'),
                (types['Equipment'], 'Dumbbell'),
                (types['Equipment'], 'Bodyweight'),
                (types['Equipment'], 'Machine'),
                (types['Equipment'], 'Cable'),
                
                # Positions
                (types['Position'], 'Standing'),
                (types['Position'], 'Seated'),
                (types['Position'], 'Lying'),
                (types['Position'], 'Inclined'),
                
                # Contraction Types
                (types['Contraction Type'], 'Concentric'),
                (types['Contraction Type'], 'Eccentric'),
                (types['Contraction Type'], 'Isometric'),
            ]
            
            for type_id, value in values_data:
                db.execute(text("""
                    INSERT INTO classification_values (classification_type_id, value, description, "order", created_at, updated_at)
                    VALUES (:type_id, :value, '', 0, NOW(), NOW())
                """), {'type_id': type_id, 'value': value})
            
            db.commit()
            print("Created classification values")
        
        print("\n=== FINAL CHECK ===")
        result = db.execute(text("""
            SELECT ct.name, COUNT(cv.id) as value_count
            FROM classification_types ct
            LEFT JOIN classification_values cv ON ct.id = cv.classification_type_id
            GROUP BY ct.id, ct.name
            ORDER BY ct.id
        """))
        
        for row in result:
            print(f"Type: {row[0]}, Values: {row[1]}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    check_and_create_classifications()
