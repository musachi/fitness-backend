#!/usr/bin/env python3
"""
Check database schema for exercises table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from src.core.database import SessionLocal

def check_exercises_table():
    db = SessionLocal()
    try:
        # Get column information
        result = db.execute(text("""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_name = 'exercises'
            ORDER BY ordinal_position
        """))
        
        print("=== EXERCISES TABLE SCHEMA ===")
        for row in result:
            print(f"Column: {row[0]}, Type: {row[1]}, Nullable: {row[2]}, Default: {row[3]}")
        
        # Check if table exists
        table_check = db.execute(text("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_name = 'exercise_classifications'
            );
        """))
        
        exists = table_check.scalar()
        print(f"\n=== exercise_classifications table exists: {exists} ===")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_exercises_table()
