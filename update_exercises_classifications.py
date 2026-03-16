#!/usr/bin/env python3
"""
Update existing exercises with classifications from Excel
"""

import pandas as pd
import sys
import os
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.crud.exercise import exercise
from src.crud.classification import classification_type, classification_value
from src.models.exercise import Exercise
from src.models.user import User
from src.models.classification import ClassificationType, ClassificationValue

# Spanish to English mappings (updated to match database)
MOVEMENT_TYPE_MAPPING = {
    "Extensión de piernas": "Leg Extension",
    "Flexión de piernas": "Leg Curl", 
    "Press de pecho": "Chest Press",
    "Remo": "Row",
    "Sentadilla": "Squat",
    "Press militar": "Military Press",
    "Curl de bíceps": "Bicep Curl",
    "Extensión de tríceps": "Tricep Extension",
    "Elevación lateral": "Lateral Raise",
    "Peso muerto": "Deadlift"
}

MUSCLE_GROUP_MAPPING = {
    "Piernas(Parte anterior)": "Legs-Anterior",
    "Piernas(Parte posterior)": "Legs-Posterior",
    "Pecho": "Chest", 
    "Espalda": "Back",
    "Hombros": "Shoulders",
    "Bíceps": "Biceps",
    "Tríceps": "Triceps",
    "Abdomen": "Abs",
    "Glúteos": "Glutes",
    "Piernas y gluteos": "Legs"
}

EQUIPMENT_MAPPING = {
    "Ejercicio con barra": "Barbell",
    "Ejercicio con mancuernas": "Dumbbell",
    "Ejercicio con maquina": "Machine",
    "Ejercicio con cables": "Cables",
    "Ejercicio con peso corporal": "Bodyweight",
    "Ejercicio con banda": "Band"
}

GOAL_MAPPING = {
    "Fuerza Máxima": "Strength",
    "Resistencia a la fuerza": "Strength Endurance", 
    "Hipertrofia": "Hypertrophy",
    "Potencia": "Power",
    "Resistencia muscular": "Muscular Endurance"
}

def find_classification_value(db: Session, classification_type_name: str, value_name: str):
    """Find existing classification value"""
    # Get classification type
    class_type = db.query(ClassificationType).filter(
        ClassificationType.name == classification_type_name
    ).first()
    
    if not class_type:
        print(f"⚠️ Classification type '{classification_type_name}' not found")
        return None
    
    # Find existing value
    value = db.query(ClassificationValue).filter(
        ClassificationValue.classification_type_id == class_type.id,
        ClassificationValue.value.ilike(value_name)
    ).first()
    
    if not value:
        print(f"⚠️ Classification value '{value_name}' not found for type '{classification_type_name}'")
        return None
    
    return value

def update_exercises_with_classifications():
    """Update existing exercises with classifications from Excel"""
    
    # Read Excel file
    excel_path = "../Libro Excel Descriptivo.xlsx"
    try:
        df = pd.read_excel(excel_path, header=1)
        print(f"📊 Excel file loaded: {df.shape[0]} rows")
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get existing exercises
        existing_exercises = db.query(Exercise).all()
        exercise_names = {ex.name.lower(): ex for ex in existing_exercises}
        
        print(f"📋 Found {len(existing_exercises)} existing exercises")
        
        updated_count = 0
        for index, row in df.head(10).iterrows():
            # Get exercise name
            exercise_name = str(row.get('Nombre del ejercicio', '')).strip()
            if not exercise_name or exercise_name.lower() == 'nan':
                continue
            
            # Find existing exercise
            exercise_obj = exercise_names.get(exercise_name.lower())
            if not exercise_obj:
                print(f"⚠️ Exercise '{exercise_name}' not found in database")
                continue
            
            print(f"\n🏋️ Updating exercise: {exercise_name} (ID: {exercise_obj.id})")
            
            # Get classifications
            classification_value_ids = []
            
            # Movement Type (from "Clasificación del ejercicio" column)
            goal = row.get('Clasificación del ejercicio')
            if pd.notna(goal) and goal:
                goal_mapped = MOVEMENT_TYPE_MAPPING.get(goal, goal)
                goal_value = find_classification_value(db, "Movement Type", goal_mapped)
                if goal_value:
                    classification_value_ids.append(goal_value.id)
                    print(f"   ✅ Movement Type: {goal_mapped}")
            
            # Other columns are empty in this Excel, so we'll add some default classifications
            # Add default Muscle Group for squat variations
            if "cuclilla" in exercise_name.lower():
                muscle_value = find_classification_value(db, "Muscle Group", "Legs-Anterior")
                if muscle_value:
                    classification_value_ids.append(muscle_value.id)
                    print(f"   ✅ Muscle Group: Legs-Anterior (default for squats)")
            
            # Add default Equipment for squats
            if "cuclilla" in exercise_name.lower():
                equipment_value = find_classification_value(db, "Equipment", "Barbell")
                if equipment_value:
                    classification_value_ids.append(equipment_value.id)
                    print(f"   ✅ Equipment: Barbell (default for squats)")
            
            # Add default Goal
            hypertrophy_value = find_classification_value(db, "Goal", "Hypertrophy")
            if hypertrophy_value:
                classification_value_ids.append(hypertrophy_value.id)
                print(f"   ✅ Goal: Hypertrophy (default)")
            
            if classification_value_ids:
                # Update exercise with classifications
                try:
                    from src.schemas.exercise import ExerciseUpdate
                    exercise_data = ExerciseUpdate(
                        classification_value_ids=classification_value_ids
                    )
                    
                    updated_exercise = exercise.update_with_relations(
                        db, db_obj=exercise_obj, obj_in=exercise_data
                    )
                    
                    print(f"   📊 Added {len(classification_value_ids)} classifications")
                    updated_count += 1
                    
                except Exception as e:
                    print(f"   ❌ Error updating exercise: {e}")
                    continue
            else:
                print(f"   ⚠️ No classifications found")
        
        print(f"\n🎉 Update completed! {updated_count} exercises updated with classifications")
        
    except Exception as e:
        print(f"❌ Update error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_exercises_with_classifications()
