#!/usr/bin/env python3
"""
Create a simple test exercise
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.database import SessionLocal
from src.models.exercise import Exercise
from src.models.classification import ClassificationValue

def create_simple_exercise():
    db = SessionLocal()
    try:
        # Get first classification values
        movement_type = db.query(ClassificationValue).join(ClassificationValue.classification_type).filter_by(name="Movement Type").first()
        muscle_group = db.query(ClassificationValue).join(ClassificationValue.classification_type).filter_by(name="Muscle Group").first()
        equipment = db.query(ClassificationValue).join(ClassificationValue.classification_type).filter_by(name="Equipment").first()
        
        print(f"Movement Type: {movement_type.value if movement_type else 'None'}")
        print(f"Muscle Group: {muscle_group.value if muscle_group else 'None'}")
        print(f"Equipment: {equipment.value if equipment else 'None'}")
        
        # Create a simple exercise
        exercise = Exercise(
            name="Test Exercise",
            short_name="Test",
            description="A simple test exercise",
            type="Strength",
            crossfit_variant=None,
            is_active=True
        )
        
        # Add classifications
        if movement_type:
            exercise.classification_values.append(movement_type)
        if muscle_group:
            exercise.classification_values.append(muscle_group)
        if equipment:
            exercise.classification_values.append(equipment)
        
        db.add(exercise)
        db.commit()
        db.refresh(exercise)
        
        print(f"✅ Created exercise: {exercise.name} (ID: {exercise.id})")
        
        # Show exercise with classifications
        loaded_exercise = db.query(Exercise).filter_by(id=exercise.id).first()
        print(f"Classifications for {loaded_exercise.name}:")
        for cv in loaded_exercise.classification_values:
            print(f"  - {cv.classification_type.name}: {cv.value}")
        
    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_simple_exercise()
