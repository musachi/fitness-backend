#!/usr/bin/env python3
"""
Check if Position and Contraction Type data exists in classification tables
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy import create_engine, text
from src.core.config import settings

def check_classification_data():
    try:
        # Connect to database
        engine = create_engine(settings.DATABASE_URL)
        
        with engine.connect() as connection:
            # Check classification types
            result = connection.execute(text("SELECT id, name FROM classification_types ORDER BY id"))
            types = result.fetchall()
            
            print("📋 Classification Types in database:")
            for type_id, name in types:
                print(f"  ID: {type_id} - Name: {name}")
            
            print()
            
            # Check if Position and Contraction Type exist
            position_type = None
            contraction_type = None
            
            for type_id, name in types:
                if "Position" in name:
                    position_type = (type_id, name)
                elif "Contraction" in name:
                    contraction_type = (type_id, name)
            
            print(f"🔍 Found Position Type: {position_type}")
            print(f"🔍 Found Contraction Type: {contraction_type}")
            
            if position_type:
                # Check Position values
                pos_result = connection.execute(text(f"SELECT id, value FROM classification_values WHERE classification_type_id = {position_type[0]} ORDER BY id"))
                positions = pos_result.fetchall()
                print(f"\n📍 Position Values ({len(positions)}):")
                for pos_id, value in positions:
                    print(f"  ID: {pos_id} - Value: {value}")
            
            if contraction_type:
                # Check Contraction Type values
                cont_result = connection.execute(text(f"SELECT id, value FROM classification_values WHERE classification_type_id = {contraction_type[0]} ORDER BY id"))
                contractions = cont_result.fetchall()
                print(f"\n💪 Contraction Type Values ({len(contractions)}):")
                for cont_id, value in contractions:
                    print(f"  ID: {cont_id} - Value: {value}")
            
            if not position_type:
                print("\n❌ Position Type not found in classification_types")
                print("   You need to create it first:")
                print("   INSERT INTO classification_types (name, description, applies_to, is_required) VALUES ('Position', 'Exercise position', 'exercise', false);")
            
            if not contraction_type:
                print("\n❌ Contraction Type not found in classification_types")
                print("   You need to create it first:")
                print("   INSERT INTO classification_types (name, description, applies_to, is_required) VALUES ('Contraction Type', 'Muscle contraction type', 'exercise', false);")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    check_classification_data()
