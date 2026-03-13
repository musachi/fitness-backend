#!/usr/bin/env python3
"""
Fix alembic version table
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy import text
from src.core.database import SessionLocal

def fix_alembic_version():
    db = SessionLocal()
    try:
        # Create alembic_version table if it doesn't exist
        db.execute(text("""
            CREATE TABLE IF NOT EXISTS alembic_version (
                version_num VARCHAR(32) NOT NULL
            )
        """))
        db.commit()
        print("Created/verified alembic_version table")
        
        # Clear alembic version table
        db.execute(text("DELETE FROM alembic_version"))
        db.commit()
        print("Cleared alembic_version table")
        
        # Set to base revision
        db.execute(text("INSERT INTO alembic_version (version_num) VALUES ('add_plan_fields')"))
        db.commit()
        print("Set alembic version to add_plan_fields")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    fix_alembic_version()
