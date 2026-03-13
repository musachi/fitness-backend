#!/usr/bin/env python3
"""
Check classification data in database
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from src.core.database import SessionLocal

def check_classification_data():
    db = SessionLocal()
    try:
        print("=== CLASSIFICATION TYPES ===")
        result = db.execute(text("SELECT id, name, applies_to FROM classification_types ORDER BY id"))
        for row in result:
            print(f"ID: {row[0]}, Name: {row[1]}, Applies to: {row[2]}")
        
        print("\n=== CLASSIFICATION VALUES ===")
        result = db.execute(text("""
            SELECT cv.id, cv.value, ct.name as type_name 
            FROM classification_values cv
            JOIN classification_types ct ON cv.classification_type_id = ct.id
            ORDER BY ct.id, cv.id
        """))
        for row in result:
            print(f"ID: {row[0]}, Value: {row[1]}, Type: {row[2]}")
        
        print("\n=== COUNTS ===")
        result = db.execute(text("SELECT name, COUNT(cv.id) as value_count FROM classification_types ct LEFT JOIN classification_values cv ON ct.id = cv.classification_type_id GROUP BY ct.id, ct.name ORDER BY ct.id"))
        for row in result:
            print(f"Type: {row[0]}, Values: {row[1]}")
        
    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_classification_data()
