#!/usr/bin/env python3
"""
Import ALL exercises from Excel file with gym-standard English names
"""

import pandas as pd
import sys
import os
from sqlalchemy.orm import Session
from src.core.database import get_db
from src.crud.exercise import exercise
from src.models.exercise import Exercise
from src.models.user import User
from src.models.classification import ClassificationType, ClassificationValue

# Gym-standard English translations
EXERCISE_NAME_MAPPING = {
    "Cuclillas": "Squat",
    "Cuclillas Cerradas": "Close Grip Squat", 
    "Cuclills Sumo": "Sumo Squat",
    "Sentadilla": "Squat",
    "Press de pecho": "Bench Press",
    "Remo": "Row",
    "Peso muerto": "Deadlift",
    "Press militar": "Military Press",
    "Curl de bíceps": "Bicep Curl",
    "Extensión de tríceps": "Tricep Extension",
    "Elevación lateral": "Lateral Raise",
    "Flexión de piernas": "Leg Curl",
    "Extensión de piernas": "Leg Extension",
    "Hip Extension": "Hip Extension",
    "Arm Extension": "Arm Extension",
    "Chest Press": "Chest Press"
}

# Movement Type mapping (Spanish to English gym terms)
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
    "Peso muerto": "Deadlift",
    "Hip Extension": "Hip Extension",
    "Arm Extension": "Arm Extension"
}

# Muscle Group mapping (Spanish to English gym terms)
MUSCLE_GROUP_MAPPING = {
    "Piernas(Parte anterior)": "Quadriceps",
    "Piernas(Parte posterior)": "Hamstrings",
    "Pecho": "Chest", 
    "Espalda": "Back",
    "Hombros": "Shoulders",
    "Bíceps": "Biceps",
    "Tríceps": "Triceps",
    "Abdomen": "Abs",
    "Glúteos": "Glutes",
    "Piernas y gluteos": "Legs and Glutes",
    "Legs-Anterior": "Quadriceps",
    "Legs-Posterior": "Hamstrings",
    "Legs": "Legs"
}

# Equipment mapping (Spanish to English gym terms)
EQUIPMENT_MAPPING = {
    "Ejercicio con barra": "Barbell",
    "Ejercicio con mancuernas": "Dumbbell",
    "Ejercicio con maquina": "Machine",
    "Ejercicio con cables": "Cables",
    "Ejercicio con peso corporal": "Bodyweight",
    "Ejercicio con banda": "Band",
    "Barbell": "Barbell",
    "Dumbbell": "Dumbbell",
    "Machine": "Machine",
    "Cables": "Cables",
    "Bodyweight": "Bodyweight",
    "Band": "Band"
}

# Goal mapping (Spanish to English gym terms)
GOAL_MAPPING = {
    "Fuerza Máxima": "Strength",
    "Resistencia a la fuerza": "Strength Endurance", 
    "Hipertrofia": "Hypertrophy",
    "Potencia": "Power",
    "Resistencia muscular": "Muscular Endurance",
    "Strength": "Strength",
    "Hypertrophy": "Hypertrophy",
    "Power": "Power"
}

# Position mapping (Static vs With Movement)
POSITION_MAPPING = {
    "Static": "Static",
    "With movement": "With Movement"
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

def translate_exercise_name(spanish_name):
    """Translate Spanish exercise name to English gym-standard name"""
    if pd.isna(spanish_name) or not spanish_name:
        return None
    
    spanish_name = str(spanish_name).strip()
    
    # Direct mapping first
    if spanish_name in EXERCISE_NAME_MAPPING:
        return EXERCISE_NAME_MAPPING[spanish_name]
    
    # Try partial matches
    for spanish_key, english_value in EXERCISE_NAME_MAPPING.items():
        if spanish_key.lower() in spanish_name.lower():
            return english_value
    
    # If no mapping found, return original (might already be English)
    return spanish_name

def get_default_classifications_for_exercise(exercise_name):
    """Get default classifications based on exercise name"""
    classifications = []
    
    exercise_lower = exercise_name.lower()
    
    # Movement Type defaults
    if "squat" in exercise_lower:
        classifications.append(("Movement Type", "Squat"))
    elif "bench" in exercise_lower or "press" in exercise_lower:
        classifications.append(("Movement Type", "Press"))
    elif "row" in exercise_lower:
        classifications.append(("Movement Type", "Row"))
    elif "deadlift" in exercise_lower:
        classifications.append(("Movement Type", "Deadlift"))
    elif "curl" in exercise_lower:
        classifications.append(("Movement Type", "Curl"))
    elif "extension" in exercise_lower:
        classifications.append(("Movement Type", "Extension"))
    elif "raise" in exercise_lower:
        classifications.append(("Movement Type", "Raise"))
    
    # Muscle Group defaults
    if "squat" in exercise_lower:
        classifications.append(("Muscle Group", "Quadriceps"))
        classifications.append(("Muscle Group", "Glutes"))
    elif "bench" in exercise_lower or "press" in exercise_lower:
        classifications.append(("Muscle Group", "Chest"))
    elif "row" in exercise_lower:
        classifications.append(("Muscle Group", "Back"))
    elif "deadlift" in exercise_lower:
        classifications.append(("Muscle Group", "Hamstrings"))
        classifications.append(("Muscle Group", "Glutes"))
        classifications.append(("Muscle Group", "Back"))
    elif "curl" in exercise_lower and "bicep" in exercise_lower:
        classifications.append(("Muscle Group", "Biceps"))
    elif "extension" in exercise_lower and "tricep" in exercise_lower:
        classifications.append(("Muscle Group", "Triceps"))
    elif "raise" in exercise_lower and "lateral" in exercise_lower:
        classifications.append(("Muscle Group", "Shoulders"))
    
    # Equipment defaults
    if "barbell" in exercise_lower or "squat" in exercise_lower or "bench" in exercise_lower or "deadlift" in exercise_lower:
        classifications.append(("Equipment", "Barbell"))
    elif "dumbbell" in exercise_lower:
        classifications.append(("Equipment", "Dumbbell"))
    elif "machine" in exercise_lower:
        classifications.append(("Equipment", "Machine"))
    elif "cable" in exercise_lower:
        classifications.append(("Equipment", "Cables"))
    elif "bodyweight" in exercise_lower:
        classifications.append(("Equipment", "Bodyweight"))
    
    # Position defaults (most exercises are dynamic)
    classifications.append(("Position", "With Movement"))
    
    # Goal defaults
    classifications.append(("Goal", "Hypertrophy"))
    
    return classifications

def import_all_exercises():
    """Import all exercises from Excel file"""
    
    # Read Excel file
    excel_path = "../Libro Excel Descriptivo.xlsx"
    try:
        df = pd.read_excel(excel_path, header=1)
        print(f"📊 Excel file loaded: {df.shape[0]} rows, {df.shape[1]} columns")
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
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
        
        # Import all exercises
        imported_count = 0
        skipped_count = 0
        error_count = 0
        
        for index, row in df.iterrows():
            # Get exercise name
            spanish_name = row.get('Nombre del ejercicio')
            if pd.isna(spanish_name) or not spanish_name or str(spanish_name).strip().lower() in ['nan', 'none', '']:
                skipped_count += 1
                continue
            
            # Translate to English
            english_name = translate_exercise_name(spanish_name)
            if not english_name:
                skipped_count += 1
                continue
            
            print(f"\n🏋️ Importing exercise {imported_count + skipped_count + 1}: {spanish_name} → {english_name}")
            
            # Check if exercise already exists
            existing_exercise = db.query(Exercise).filter(
                Exercise.name.ilike(english_name)
            ).first()
            
            if existing_exercise:
                print(f"⚠️ Exercise '{english_name}' already exists (ID: {existing_exercise.id})")
                skipped_count += 1
                continue
            
            # Get classifications from Excel
            classifications = []
            
            # Movement Type from Excel
            movement_type = row.get('Clasificación del ejercicio')
            if pd.notna(movement_type) and movement_type:
                movement_mapped = MOVEMENT_TYPE_MAPPING.get(movement_type, movement_type)
                movement_value = find_classification_value(db, "Movement Type", movement_mapped)
                if movement_value:
                    classifications.append(movement_value.id)
                    print(f"   ✅ Movement Type: {movement_mapped}")
            
            # Add default classifications based on exercise name
            default_classifications = get_default_classifications_for_exercise(english_name)
            for class_type_name, class_value in default_classifications:
                class_value_obj = find_classification_value(db, class_type_name, class_value)
                if class_value_obj and class_value_obj.id not in classifications:
                    classifications.append(class_value_obj.id)
                    print(f"   ✅ {class_type_name}: {class_value} (default)")
            
            # Create exercise
            try:
                from src.schemas.exercise import ExerciseCreate
                exercise_data = ExerciseCreate(
                    name=english_name,
                    short_name=english_name[:20] if len(english_name) > 20 else english_name,
                    description=f"Imported from Excel - {spanish_name}",
                    classification_value_ids=classifications
                )
                
                created_exercise = exercise.create_with_relations(
                    db, obj_in=exercise_data, coach_id=admin_user.id
                )
                
                print(f"✅ Exercise created: {created_exercise.name} (ID: {created_exercise.id})")
                print(f"   📊 Classifications: {len(classifications)} assigned")
                
                imported_count += 1
                
            except Exception as e:
                print(f"❌ Error creating exercise '{english_name}': {e}")
                error_count += 1
                continue
        
        print(f"\n🎉 Import completed!")
        print(f"   ✅ Successfully imported: {imported_count} exercises")
        print(f"   ⚠️ Skipped (duplicates/invalid): {skipped_count} exercises")
        print(f"   ❌ Errors: {error_count} exercises")
        
    except Exception as e:
        print(f"❌ Import error: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_all_exercises()
