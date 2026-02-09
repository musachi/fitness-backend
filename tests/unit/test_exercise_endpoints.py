from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.exercise import Equipment, Exercise, ExerciseCategory, MuscleGroup
from src.models.user import User


class TestExerciseEndpoints:
    """Test suite for exercise endpoints."""

    def test_read_exercises_empty(self, client: TestClient, db_session: Session):
        """Test reading exercises when database is empty."""
        response = client.get("/api/v1/exercises/")
        assert response.status_code == 200
        data = response.json()
        assert data["exercises"] == []
        assert data["total"] == 0
        assert data["page"] == 1
        assert data["size"] == 100

    def test_read_exercises_with_data(
        self, client: TestClient, test_exercise: Exercise
    ):
        """Test reading exercises with existing data."""
        response = client.get("/api/v1/exercises/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["exercises"]) == 1
        assert data["total"] == 1
        assert data["exercises"][0]["name"] == "Bench Press"

    def test_read_exercise_by_id(self, client: TestClient, test_exercise: Exercise):
        """Test getting a specific exercise by ID."""
        response = client.get(f"/api/v1/exercises/{test_exercise.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == test_exercise.id
        assert data["name"] == "Bench Press"
        assert data["short_name"] == "BP"

    def test_read_exercise_not_found(self, client: TestClient):
        """Test getting a non-existent exercise."""
        response = client.get("/api/v1/exercises/99999")
        assert response.status_code == 404
        assert "Exercise not found" in response.json()["detail"]

    def test_create_exercise_unauthorized(self, client: TestClient):
        """Test creating exercise without authentication."""
        exercise_data = {"name": "New Exercise", "description": "Test exercise"}
        response = client.post("/api/v1/exercises/", json=exercise_data)
        assert response.status_code == 401

    def test_create_exercise_authorized(
        self, client: TestClient, auth_headers, test_user: User
    ):
        """Test creating exercise with authentication."""
        exercise_data = {
            "name": "New Exercise",
            "short_name": "NE",
            "description": "Test exercise",
            "type": "strength",
        }
        response = client.post(
            "/api/v1/exercises/", json=exercise_data, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "New Exercise"
        assert data["coach_id"] == str(test_user.id)

    def test_update_exercise_unauthorized(
        self, client: TestClient, test_exercise: Exercise
    ):
        """Test updating exercise without authentication."""
        update_data = {"name": "Updated Exercise"}
        response = client.put(f"/api/v1/exercises/{test_exercise.id}", json=update_data)
        assert response.status_code == 401

    def test_update_exercise_authorized_owner(
        self, client: TestClient, auth_headers, test_exercise: Exercise
    ):
        """Test updating exercise as owner."""
        update_data = {"name": "Updated Exercise"}
        response = client.put(
            f"/api/v1/exercises/{test_exercise.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Exercise"

    def test_update_exercise_not_found(self, client: TestClient, auth_headers):
        """Test updating non-existent exercise."""
        update_data = {"name": "Updated Exercise"}
        response = client.put(
            "/api/v1/exercises/99999", json=update_data, headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_exercise_unauthorized(
        self, client: TestClient, test_exercise: Exercise
    ):
        """Test deleting exercise without authentication."""
        response = client.delete(f"/api/v1/exercises/{test_exercise.id}")
        assert response.status_code == 401

    def test_delete_exercise_authorized_owner(
        self, client: TestClient, auth_headers, test_exercise: Exercise
    ):
        """Test deleting exercise as owner."""
        response = client.delete(
            f"/api/v1/exercises/{test_exercise.id}", headers=auth_headers
        )
        assert response.status_code == 204

    def test_delete_exercise_not_found(self, client: TestClient, auth_headers):
        """Test deleting non-existent exercise."""
        response = client.delete("/api/v1/exercises/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_search_exercises(self, client: TestClient, test_exercise: Exercise):
        """Test searching exercises."""
        response = client.get("/api/v1/exercises/?search=Bench")
        assert response.status_code == 200
        data = response.json()
        assert len(data["exercises"]) == 1
        assert "Bench" in data["exercises"][0]["name"]

    def test_filter_exercises_by_category(
        self,
        client: TestClient,
        test_exercise: Exercise,
        exercise_category: ExerciseCategory,
    ):
        """Test filtering exercises by category."""
        response = client.get(f"/api/v1/exercises/?category_id={exercise_category.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["exercises"]) == 1
        assert data["exercises"][0]["category_id"] == exercise_category.id

    def test_filter_exercises_by_muscle_group(
        self, client: TestClient, test_exercise: Exercise, muscle_group: MuscleGroup
    ):
        """Test filtering exercises by muscle group."""
        response = client.get(f"/api/v1/exercises/?muscle_group_id={muscle_group.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["exercises"]) == 1
        assert data["exercises"][0]["muscle_group_id"] == muscle_group.id

    def test_filter_exercises_by_equipment(
        self, client: TestClient, test_exercise: Exercise, equipment: Equipment
    ):
        """Test filtering exercises by equipment."""
        response = client.get(f"/api/v1/exercises/?equipment_id={equipment.id}")
        assert response.status_code == 200
        data = response.json()
        assert len(data["exercises"]) == 1
        assert data["exercises"][0]["equipment_id"] == equipment.id

    def test_get_my_exercises(
        self, client: TestClient, auth_headers, test_exercise: Exercise, test_user: User
    ):
        """Test getting exercises created by current coach."""
        response = client.get("/api/v1/exercises/coach/mine", headers=auth_headers)
        assert response.status_code == 200
        data = response.json()
        assert len(data["exercises"]) == 1
        assert data["exercises"][0]["coach_id"] == str(test_user.id)

    def test_pagination(self, client: TestClient, db_session: Session, test_user: User):
        """Test exercise pagination."""
        # Create multiple exercises
        for i in range(15):
            exercise = Exercise(
                name=f"Exercise {i}",
                coach_id=test_user.id,
                description=f"Description {i}",
            )
            db_session.add(exercise)
        db_session.commit()

        # Test first page
        response = client.get("/api/v1/exercises/?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["exercises"]) == 10
        assert data["page"] == 1
        assert data["size"] == 10

        # Test second page
        response = client.get("/api/v1/exercises/?skip=10&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["exercises"]) == 5
        assert data["page"] == 2
