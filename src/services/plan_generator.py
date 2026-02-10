from __future__ import annotations

from datetime import date, timedelta
from typing import Dict, List, Optional
from sqlalchemy.orm import Session
import random

from src.models.plan import Plan, WorkoutSession, WorkoutExercise
from src.models.exercise import Exercise
from src.schemas.plan import PlanGoal, PlanLevel, WorkoutFocus, PlanCreate, PlanResponse


class PlanTemplate:
    """Template para generar planes automáticamente."""

    def __init__(
        self,
        name: str,
        description: str,
        goal: PlanGoal,
        level: PlanLevel,
        duration_weeks: int,
        workouts_per_week: int,
        focus_rotation: List[WorkoutFocus],
        exercise_rules: Dict[str, List[str]],
        progression_rules: Dict[str, any] = None
    ):
        self.name = name
        self.description = description
        self.goal = goal
        self.level = level
        self.duration_weeks = duration_weeks
        self.workouts_per_week = workouts_per_week
        self.focus_rotation = focus_rotation
        self.exercise_rules = exercise_rules
        self.progression_rules = progression_rules or {}


# Templates predefinidos
BEGINNER_FULL_BODY = PlanTemplate(
    name="Beginner Full Body",
    description="Full body workout 3x per week for beginners",
    goal=PlanGoal.GENERAL_FITNESS,
    level=PlanLevel.BEGINNER,
    duration_weeks=4,
    workouts_per_week=3,
    focus_rotation=[
        WorkoutFocus.FULL_BODY,
        WorkoutFocus.REST,
        WorkoutFocus.FULL_BODY,
        WorkoutFocus.REST,
        WorkoutFocus.FULL_BODY,
        WorkoutFocus.REST,
        WorkoutFocus.REST
    ],
    exercise_rules={
        "compound": ["squat", "bench_press", "deadlift", "overhead_press", "pull_up"],
        "accessory": ["bicep_curl", "tricep_extension", "calf_raise", "plank"]
    }
)

PPL_INTERMEDIATE = PlanTemplate(
    name="Push Pull Legs Intermediate",
    description="6-day PPL split for intermediate lifters",
    goal=PlanGoal.MUSCLE_GAIN,
    level=PlanLevel.INTERMEDIATE,
    duration_weeks=8,
    workouts_per_week=6,
    focus_rotation=[
        WorkoutFocus.PUSH,
        WorkoutFocus.PULL,
        WorkoutFocus.LEGS,
        WorkoutFocus.PUSH,
        WorkoutFocus.PULL,
        WorkoutFocus.LEGS,
        WorkoutFocus.REST
    ],
    exercise_rules={
        "push": ["bench_press", "overhead_press", "dumbbell_press", "dips", "push_up"],
        "pull": ["pull_up", "deadlift", "barbell_row", "lat_pulldown", "face_pull"],
        "legs": ["squat", "leg_press", "lunges", "calf_raise", "leg_curl"]
    }
)

UPPER_LOWER_ADVANCED = PlanTemplate(
    name="Upper Lower Advanced",
    description="4-day upper/lower split for advanced athletes",
    goal=PlanGoal.STRENGTH,
    level=PlanLevel.ADVANCED,
    duration_weeks=12,
    workouts_per_week=4,
    focus_rotation=[
        WorkoutFocus.UPPER_BODY,
        WorkoutFocus.LOWER_BODY,
        WorkoutFocus.REST,
        WorkoutFocus.UPPER_BODY,
        WorkoutFocus.LOWER_BODY,
        WorkoutFocus.REST,
        WorkoutFocus.REST
    ],
    exercise_rules={
        "upper": ["bench_press", "overhead_press", "barbell_row", "pull_up", "dips"],
        "lower": ["squat", "deadlift", "leg_press", "lunges", "calf_raise"]
    }
)


class PlanGenerator:
    """Genera planes de entrenamiento basados en templates."""

    def __init__(self, db_session: Session):
        self.db = db_session
        self.templates = {
            "beginner_full_body": BEGINNER_FULL_BODY,
            "ppl_intermediate": PPL_INTERMEDIATE,
            "upper_lower_advanced": UPPER_LOWER_ADVANCED
        }

    def generate_plan_from_template(
        self,
        template_name: str,
        user_id: str,
        custom_name: Optional[str] = None
    ) -> Plan:
        """Genera un plan completo desde un template."""

        template = self.templates.get(template_name)
        if not template:
            raise ValueError(f"Template '{template_name}' not found")

        # Crear plan base
        plan = Plan(
            name=custom_name or template.name,
            description=template.description,
            goal=template.goal.value,
            level=template.level.value,
            duration_weeks=template.duration_weeks,
            coach_id=user_id
        )

        self.db.add(plan)
        self.db.flush()  # Para obtener el ID

        # Generar workouts para cada día
        day_counter = 0
        start_date = date.today()

        for week in range(1, template.duration_weeks + 1):
            for day in range(1, 8):  # 7 días por semana
                focus = template.focus_rotation[(day_counter % len(template.focus_rotation))]

                if focus != WorkoutFocus.REST:
                    workout_date = start_date + timedelta(days=day_counter)

                    session = WorkoutSession(
                        plan_id=plan.id,
                        client_id=user_id,
                        date=workout_date,
                        completed=False,
                        notes=f"Week {week}, Day {day} - {focus.value.title()}"
                    )

                    # Agregar ejercicios
                    exercises = self._select_exercises_for_focus(focus, template, week)
                    for i, exercise_config in enumerate(exercises):
                        workout_exercise = WorkoutExercise(
                            session=session,
                            exercise_id=exercise_config["exercise_id"],
                            sets_planned=exercise_config.get("sets", 3),
                            reps_planned=exercise_config.get("reps", "8-12"),
                            weight_planned=exercise_config.get("weight", "bodyweight"),
                            rest_between_sets=exercise_config.get("rest", "60s")
                        )
                        session.workout_exercises.append(workout_exercise)

                    self.db.add(session)

                day_counter += 1

        self.db.commit()
        return plan

    def _select_exercises_for_focus(
        self,
        focus: WorkoutFocus,
        template: PlanTemplate,
        week_number: int
    ) -> List[Dict[str, any]]:
        """Selecciona ejercicios apropiados para el focus del día."""

        # Obtener ejercicios disponibles
        exercises = self.db.query(Exercise).all()
        exercise_map = {ex.name.lower().replace(" ", "_"): ex for ex in exercises}

        selected_exercises = []

        if focus == WorkoutFocus.FULL_BODY:
            # Full body: compound + accessory
            compound_exercises = ["squat", "bench_press", "deadlift", "overhead_press"]
            accessory_exercises = ["bicep_curl", "tricep_extension", "calf_raise"]

            # Seleccionar 2-3 compound exercises
            for compound in compound_exercises[:3]:
                if compound in exercise_map:
                    selected_exercises.append({
                        "exercise_id": exercise_map[compound].id,
                        "sets": 3,
                        "reps": "8-12" if template.level == PlanLevel.BEGINNER else "6-10",
                        "weight": "moderate",
                        "rest": "90s"
                    })

            # Seleccionar 1-2 accessory exercises
            for accessory in random.sample(accessory_exercises, min(2, len(accessory_exercises))):
                if accessory in exercise_map:
                    selected_exercises.append({
                        "exercise_id": exercise_map[accessory].id,
                        "sets": 2,
                        "reps": "10-15",
                        "weight": "light",
                        "rest": "60s"
                    })

        elif focus == WorkoutFocus.PUSH:
            push_exercises = ["bench_press", "overhead_press", "dumbbell_press", "dips"]
            for exercise in push_exercises[:4]:
                if exercise in exercise_map:
                    selected_exercises.append({
                        "exercise_id": exercise_map[exercise].id,
                        "sets": 4 if template.level == PlanLevel.ADVANCED else 3,
                        "reps": "8-12" if template.goal == PlanGoal.MUSCLE_GAIN else "6-8",
                        "weight": "moderate",
                        "rest": "90s"
                    })

        elif focus == WorkoutFocus.PULL:
            pull_exercises = ["pull_up", "deadlift", "barbell_row", "lat_pulldown"]
            for exercise in pull_exercises[:4]:
                if exercise in exercise_map:
                    selected_exercises.append({
                        "exercise_id": exercise_map[exercise].id,
                        "sets": 4 if template.level == PlanLevel.ADVANCED else 3,
                        "reps": "8-12" if template.goal == PlanGoal.MUSCLE_GAIN else "5-8",
                        "weight": "moderate",
                        "rest": "90s"
                    })

        elif focus == WorkoutFocus.LEGS:
            leg_exercises = ["squat", "leg_press", "lunges", "calf_raise"]
            for exercise in leg_exercises[:4]:
                if exercise in exercise_map:
                    selected_exercises.append({
                        "exercise_id": exercise_map[exercise].id,
                        "sets": 4 if template.level == PlanLevel.ADVANCED else 3,
                        "reps": "10-15" if template.goal == PlanGoal.WEIGHT_LOSS else "8-12",
                        "weight": "moderate",
                        "rest": "90s"
                    })

        elif focus == WorkoutFocus.UPPER_BODY:
            upper_exercises = ["bench_press", "overhead_press", "barbell_row", "pull_up"]
            for exercise in upper_exercises[:4]:
                if exercise in exercise_map:
                    selected_exercises.append({
                        "exercise_id": exercise_map[exercise].id,
                        "sets": 4,
                        "reps": "6-10",
                        "weight": "heavy",
                        "rest": "120s"
                    })

        elif focus == WorkoutFocus.LOWER_BODY:
            lower_exercises = ["squat", "deadlift", "leg_press", "lunges"]
            for exercise in lower_exercises[:4]:
                if exercise in exercise_map:
                    selected_exercises.append({
                        "exercise_id": exercise_map[exercise].id,
                        "sets": 4,
                        "reps": "5-8",
                        "weight": "heavy",
                        "rest": "120s"
                    })

        # Si no se encontraron ejercicios, agregar algunos genéricos
        if not selected_exercises and exercises:
            for i, exercise in enumerate(exercises[:3]):
                selected_exercises.append({
                    "exercise_id": exercise.id,
                    "sets": 3,
                    "reps": "8-12",
                    "weight": "moderate",
                    "rest": "60s"
                })

        return selected_exercises

    def get_available_templates(self) -> List[Dict[str, any]]:
        """Retorna la lista de templates disponibles."""
        templates = []
        for key, template in self.templates.items():
            templates.append({
                "template_key": key,
                "name": template.name,
                "description": template.description,
                "goal": template.goal.value,
                "level": template.level.value,
                "duration_weeks": template.duration_weeks,
                "workouts_per_week": template.workouts_per_week,
                "focus_rotation": [focus.value for focus in template.focus_rotation]
            })
        return templates

    def create_custom_plan(self, plan_data: PlanCreate, user_id: str) -> Plan:
        """Crea un plan personalizado (básico por ahora)."""

        plan = Plan(
            name=plan_data.name,
            description=plan_data.description,
            goal=plan_data.goal.value,
            level=plan_data.level.value,
            duration_weeks=plan_data.duration_weeks,
            coach_id=user_id
        )

        self.db.add(plan)
        self.db.commit()
        self.db.refresh(plan)

        return plan
