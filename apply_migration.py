#!/usr/bin/env python3
"""
Apply exercise dynamic fields migration manually
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from src.core.database import SessionLocal

def apply_migration():
    db = SessionLocal()
    try:
        # Add is_active column to exercises table
        db.execute(text("""
            ALTER TABLE exercises 
            ADD COLUMN IF NOT EXISTS is_active BOOLEAN DEFAULT TRUE
        """))
        db.commit()
        print("Added is_active column to exercises table")
        
        # Create exercise_classifications table
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS exercise_classifications (
                exercise_id INTEGER NOT NULL,
                classification_value_id INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT now(),
                PRIMARY KEY (exercise_id, classification_value_id),
                FOREIGN KEY (exercise_id) REFERENCES exercises(id),
                FOREIGN KEY (classification_value_id) REFERENCES classification_values(id)
            )
        """))
        db.commit()
        print("Created exercise_classifications table")
        
        print("Migration applied successfully!")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    apply_migration()
