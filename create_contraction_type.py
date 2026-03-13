#!/usr/bin/env python3
"""
Create Contraction Type classification and add some common values
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from src.core.config import settings

def create_contraction_type():
    try:
        # Connect to database
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            # Start transaction
            trans = connection.begin()
            
            try:
                # Create Contraction Type classification
                print("📝 Creating Contraction Type classification...")
                result = connection.execute(text("""
                    INSERT INTO classification_types (name, description, applies_to, is_required)
                    VALUES ('Contraction Type', 'Muscle contraction type', 'exercise', false)
                    RETURNING id
                """))
                contraction_type_id = result.fetchone()[0]
                print(f"✅ Created Contraction Type with ID: {contraction_type_id}")
                
                # Add common contraction types
                contraction_values = [
                    "Concentric",
                    "Eccentric", 
                    "Isometric",
                    "Isotonic",
                    "Isokinetic"
                ]
                
                print("\n💪 Adding contraction type values...")
                for i, value in enumerate(contraction_values, 1):
                    connection.execute(text("""
                        INSERT INTO classification_values (classification_type_id, value, description, "order")
                        VALUES (:type_id, :value, :description, :order)
                    """), {
                        'type_id': contraction_type_id,
                        'value': value,
                        'description': f"{value} contraction type",
                        'order': i
                    })
                    print(f"  ✅ Added: {value}")
                
                # Commit transaction
                trans.commit()
                print(f"\n🎉 Successfully created Contraction Type with {len(contraction_values)} values!")
                
            except Exception as e:
                trans.rollback()
                raise e
                
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    create_contraction_type()
