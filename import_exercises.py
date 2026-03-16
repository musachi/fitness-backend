#!/usr/bin/env python3
"""
Import exercises from Excel file
Imports first 10 exercises from "Libro Excel Descriptivo.xlsx" and assigns them to admin user
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

# Spanish to English mappings
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

def find_or_create_classification_value(db: Session, classification_type_name: str, value_name: str):
    """Find existing classification value or create new one"""
    # Get classification type
    from src.models.classification import ClassificationType, ClassificationValue
    
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

def clean_exercise_name(name):
    """Clean exercise name from Excel"""
    if pd.isna(name) or not name:
        return None
    
    # Remove extra spaces and clean
    name = str(name).strip()
    if not name or name.lower() in ['nan', 'none', '']:
        return None
    
    return name

def import_exercises_from_excel():
    """Import exercises from Excel file"""
    
    # Read Excel file
    excel_path = "../Libro Excel Descriptivo.xlsx"
    try:
        df = pd.read_excel(excel_path, header=1)
        print(f"📊 Excel file loaded: {df.shape[0]} rows, {df.shape[1]} columns")
        print(f"📋 Columns: {df.columns.tolist()}")
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        print(f"📁 Looking for file at: {os.path.abspath(excel_path)}")
        return
    
    # Get database session
    db = next(get_db())
    
    try:
        # Get admin user
        admin_user = db.query(User).filter(User.role_id == 1).first()
        if not admin_user:
            print("❌ Admin user not found")
            return
        
        print(f"👤 Admin user found: {admin_user.name} (ID: {admin_user.id})")
        
        # Import first 10 exercises
        imported_count = 0
        for index, row in df.head(10).iterrows():
            # Get exercise name
            exercise_name = clean_exercise_name(row.get('Nombre del ejercicio'))
            if not exercise_name:
                print(f"⚠️ Row {index}: No valid exercise name found")
                continue
            
            print(f"\n🏋️ Importing exercise {index + 1}: {exercise_name}")
            
            # Get classifications
            classifications = []
            
            # Movement Type
            movement_type = row.get('Por movimiento')
            if pd.notna(movement_type) and movement_type:
                movement_mapped = MOVEMENT_TYPE_MAPPING.get(movement_type, movement_type)
                movement_value = find_or_create_classification_value(db, "Movement Type", movement_mapped)
                if movement_value:
                    classifications.append(movement_value.id)
            
            # Muscle Group
            muscle_group = row.get('Por Plano Muscular')
            if pd.notna(muscle_group) and muscle_group:
                muscle_mapped = MUSCLE_GROUP_MAPPING.get(muscle_group, muscle_group)
                muscle_value = find_or_create_classification_value(db, "Muscle Group", muscle_mapped)
                if muscle_value:
                    classifications.append(muscle_value.id)
            
            # Equipment
            equipment = row.get('Por implemento')
            if pd.notna(equipment) and equipment:
                equipment_mapped = EQUIPMENT_MAPPING.get(equipment, equipment)
                equipment_value = find_or_create_classification_value(db, "Equipment", equipment_mapped)
                if equipment_value:
                    classifications.append(equipment_value.id)
            
            # Goal
            goal = row.get('Clasificación del ejercicio')
            if pd.notna(goal) and goal:
                goal_mapped = GOAL_MAPPING.get(goal, goal)
                goal_value = find_or_create_classification_value(db, "Goal", goal_mapped)
                if goal_value:
                    classifications.append(goal_value.id)
            
            # Check if exercise already exists
            existing_exercise = db.query(Exercise).filter(
                Exercise.name.ilike(exercise_name)
            ).first()
            
            if existing_exercise:
                print(f"⚠️ Exercise '{exercise_name}' already exists (ID: {existing_exercise.id})")
                continue
            
            # Create exercise
            try:
                from src.schemas.exercise import ExerciseCreate
                exercise_data = ExerciseCreate(
                    name=exercise_name,
                    short_name=exercise_name[:20] if len(exercise_name) > 20 else exercise_name,
                    description=f"Imported from Excel - {row.get('Clasificación del ejercicio', 'N/A')}",
                    classification_value_ids=classifications
                )
                
                created_exercise = exercise.create_with_relations(
                    db, obj_in=exercise_data, coach_id=admin_user.id
                )
                
                print(f"✅ Exercise created: {created_exercise.name} (ID: {created_exercise.id})")
                print(f"   📊 Classifications: {len(classifications)} assigned")
                
                imported_count += 1
                
            except Exception as e:
                print(f"❌ Error creating exercise '{exercise_name}': {e}")
                continue
        
        print(f"\n🎉 Import completed! {imported_count} exercises imported successfully")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_exercises_from_excel()
