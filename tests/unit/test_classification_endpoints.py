from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from src.models.exercise import (
    ContractionType,
    Equipment,
    ExerciseCategory,
    MovementType,
    MuscleGroup,
    Position,
)


class TestExerciseCategoryEndpoints:
    """Test suite for exercise category endpoints."""

    def test_read_categories_empty(self, client: TestClient):
        """Test reading categories when database is empty."""
        response = client.get("/api/v1/exercises/categories/")
        assert response.status_code == 200
        data = response.json()
        assert data["categories"] == []
        assert data["total"] == 0

    def test_read_categories_with_data(
        self, client: TestClient, exercise_category: ExerciseCategory
    ):
        """Test reading categories with existing data."""
        response = client.get("/api/v1/exercises/categories/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 1
        assert data["total"] == 1
        assert data["categories"][0]["name"] == "Strength"

    def test_read_category_by_id(
        self, client: TestClient, exercise_category: ExerciseCategory
    ):
        """Test getting a specific category by ID."""
        response = client.get(f"/api/v1/exercises/categories/{exercise_category.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == exercise_category.id
        assert data["name"] == "Strength"
        assert data["displacement"] is False

    def test_read_category_not_found(self, client: TestClient):
        """Test getting a non-existent category."""
        response = client.get("/api/v1/exercises/categories/99999")
        assert response.status_code == 404
        assert "Category not found" in response.json()["detail"]

    def test_create_category_unauthorized(self, client: TestClient):
        """Test creating category without authentication."""
        category_data = {"name": "Cardio", "displacement": True}
        response = client.post("/api/v1/exercises/categories/", json=category_data)
        assert response.status_code == 401

    def test_create_category_authorized(self, client: TestClient, auth_headers):
        """Test creating category with authentication."""
        category_data = {
            "name": "Cardio",
            "displacement": True,
            "metabolic_type": "aerobic",
        }
        response = client.post(
            "/api/v1/exercises/categories/", json=category_data, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Cardio"
        assert data["displacement"] is True
        assert data["metabolic_type"] == "aerobic"

    def test_create_category_duplicate_name(
        self, client: TestClient, auth_headers, exercise_category: ExerciseCategory
    ):
        """Test creating category with duplicate name."""
        category_data = {"name": "Strength"}  # Same as existing
        response = client.post(
            "/api/v1/exercises/categories/", json=category_data, headers=auth_headers
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_update_category_unauthorized(
        self, client: TestClient, exercise_category: ExerciseCategory
    ):
        """Test updating category without authentication."""
        update_data = {"name": "Updated Category"}
        response = client.put(
            f"/api/v1/exercises/categories/{exercise_category.id}", json=update_data
        )
        assert response.status_code == 401

    def test_update_category_authorized(
        self, client: TestClient, auth_headers, exercise_category: ExerciseCategory
    ):
        """Test updating category with authentication."""
        update_data = {"name": "Updated Category", "displacement": True}
        response = client.put(
            f"/api/v1/exercises/categories/{exercise_category.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Category"
        assert data["displacement"] is True

    def test_update_category_duplicate_name(
        self, client: TestClient, auth_headers, db_session: Session
    ):
        """Test updating category with duplicate name."""
        # Create two categories
        cat1 = ExerciseCategory(name="Category 1")
        cat2 = ExerciseCategory(name="Category 2")
        db_session.add_all([cat1, cat2])
        db_session.commit()

        # Try to update cat1 with cat2's name
        update_data = {"name": "Category 2"}
        response = client.put(
            f"/api/v1/exercises/categories/{cat1.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_update_category_not_found(self, client: TestClient, auth_headers):
        """Test updating non-existent category."""
        update_data = {"name": "Updated Category"}
        response = client.put(
            "/api/v1/exercises/categories/99999", json=update_data, headers=auth_headers
        )
        assert response.status_code == 404

    def test_delete_category_unauthorized(
        self, client: TestClient, exercise_category: ExerciseCategory
    ):
        """Test deleting category without authentication."""
        response = client.delete(f"/api/v1/exercises/categories/{exercise_category.id}")
        assert response.status_code == 401

    def test_delete_category_authorized(
        self, client: TestClient, auth_headers, exercise_category: ExerciseCategory
    ):
        """Test deleting category with authentication."""
        response = client.delete(
            f"/api/v1/exercises/categories/{exercise_category.id}", headers=auth_headers
        )
        assert response.status_code == 204

    def test_delete_category_not_found(self, client: TestClient, auth_headers):
        """Test deleting non-existent category."""
        response = client.delete(
            "/api/v1/exercises/categories/99999", headers=auth_headers
        )
        assert response.status_code == 404


class TestMovementTypeEndpoints:
    """Test suite for movement type endpoints."""

    def test_read_movement_types_empty(self, client: TestClient):
        """Test reading movement types when database is empty."""
        response = client.get("/api/v1/exercises/movement-types/")
        assert response.status_code == 200
        data = response.json()
        assert data["movement_types"] == []
        assert data["total"] == 0

    def test_read_movement_types_with_data(
        self, client: TestClient, movement_type: MovementType
    ):
        """Test reading movement types with existing data."""
        response = client.get("/api/v1/exercises/movement-types/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["movement_types"]) == 1
        assert data["total"] == 1
        assert data["movement_types"][0]["name"] == "Compound"

    def test_read_movement_type_by_id(
        self, client: TestClient, movement_type: MovementType
    ):
        """Test getting a specific movement type by ID."""
        response = client.get(f"/api/v1/exercises/movement-types/{movement_type.id}")
        assert response.status_code == 200
        data = response.json()
        assert data["id"] == movement_type.id
        assert data["name"] == "Compound"

    def test_create_movement_type_authorized(self, client: TestClient, auth_headers):
        """Test creating movement type with authentication."""
        movement_type_data = {"name": "Isolation"}
        response = client.post(
            "/api/v1/exercises/movement-types/",
            json=movement_type_data,
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Isolation"

    def test_create_movement_type_duplicate_name(
        self, client: TestClient, auth_headers, movement_type: MovementType
    ):
        """Test creating movement type with duplicate name."""
        movement_type_data = {"name": "Compound"}  # Same as existing
        response = client.post(
            "/api/v1/exercises/movement-types/",
            json=movement_type_data,
            headers=auth_headers,
        )
        assert response.status_code == 400
        assert "already exists" in response.json()["detail"]

    def test_update_movement_type_authorized(
        self, client: TestClient, auth_headers, movement_type: MovementType
    ):
        """Test updating movement type with authentication."""
        update_data = {"name": "Updated Movement Type"}
        response = client.put(
            f"/api/v1/exercises/movement-types/{movement_type.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Movement Type"

    def test_delete_movement_type_authorized(
        self, client: TestClient, auth_headers, movement_type: MovementType
    ):
        """Test deleting movement type with authentication."""
        response = client.delete(
            f"/api/v1/exercises/movement-types/{movement_type.id}", headers=auth_headers
        )
        assert response.status_code == 204


class TestMuscleGroupEndpoints:
    """Test suite for muscle group endpoints."""

    def test_read_muscle_groups_empty(self, client: TestClient):
        """Test reading muscle groups when database is empty."""
        response = client.get("/api/v1/exercises/muscle-groups/")
        assert response.status_code == 200
        data = response.json()
        assert data["muscle_groups"] == []
        assert data["total"] == 0

    def test_read_muscle_groups_with_data(
        self, client: TestClient, muscle_group: MuscleGroup
    ):
        """Test reading muscle groups with existing data."""
        response = client.get("/api/v1/exercises/muscle-groups/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["muscle_groups"]) == 1
        assert data["total"] == 1
        assert data["muscle_groups"][0]["name"] == "Chest"

    def test_create_muscle_group_authorized(self, client: TestClient, auth_headers):
        """Test creating muscle group with authentication."""
        muscle_group_data = {"name": "Back"}
        response = client.post(
            "/api/v1/exercises/muscle-groups/",
            json=muscle_group_data,
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Back"

    def test_update_muscle_group_authorized(
        self, client: TestClient, auth_headers, muscle_group: MuscleGroup
    ):
        """Test updating muscle group with authentication."""
        update_data = {"name": "Updated Muscle Group"}
        response = client.put(
            f"/api/v1/exercises/muscle-groups/{muscle_group.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Muscle Group"

    def test_delete_muscle_group_authorized(
        self, client: TestClient, auth_headers, muscle_group: MuscleGroup
    ):
        """Test deleting muscle group with authentication."""
        response = client.delete(
            f"/api/v1/exercises/muscle-groups/{muscle_group.id}", headers=auth_headers
        )
        assert response.status_code == 204


class TestEquipmentEndpoints:
    """Test suite for equipment endpoints."""

    def test_read_equipment_empty(self, client: TestClient):
        """Test reading equipment when database is empty."""
        response = client.get("/api/v1/exercises/equipment/")
        assert response.status_code == 200
        data = response.json()
        assert data["equipment"] == []
        assert data["total"] == 0

    def test_read_equipment_with_data(self, client: TestClient, equipment: Equipment):
        """Test reading equipment with existing data."""
        response = client.get("/api/v1/exercises/equipment/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["equipment"]) == 1
        assert data["total"] == 1
        assert data["equipment"][0]["name"] == "Barbell"

    def test_create_equipment_authorized(self, client: TestClient, auth_headers):
        """Test creating equipment with authentication."""
        equipment_data = {"name": "Dumbbell"}
        response = client.post(
            "/api/v1/exercises/equipment/", json=equipment_data, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Dumbbell"

    def test_update_equipment_authorized(
        self, client: TestClient, auth_headers, equipment: Equipment
    ):
        """Test updating equipment with authentication."""
        update_data = {"name": "Updated Equipment"}
        response = client.put(
            f"/api/v1/exercises/equipment/{equipment.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Equipment"

    def test_delete_equipment_authorized(
        self, client: TestClient, auth_headers, equipment: Equipment
    ):
        """Test deleting equipment with authentication."""
        response = client.delete(
            f"/api/v1/exercises/equipment/{equipment.id}", headers=auth_headers
        )
        assert response.status_code == 204


class TestPositionEndpoints:
    """Test suite for position endpoints."""

    def test_read_positions_empty(self, client: TestClient):
        """Test reading positions when database is empty."""
        response = client.get("/api/v1/exercises/positions/")
        assert response.status_code == 200
        data = response.json()
        assert data["positions"] == []
        assert data["total"] == 0

    def test_read_positions_with_data(self, client: TestClient, position: Position):
        """Test reading positions with existing data."""
        response = client.get("/api/v1/exercises/positions/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["positions"]) == 1
        assert data["total"] == 1
        assert data["positions"][0]["name"] == "Standing"

    def test_create_position_authorized(self, client: TestClient, auth_headers):
        """Test creating position with authentication."""
        position_data = {"name": "Seated"}
        response = client.post(
            "/api/v1/exercises/positions/", json=position_data, headers=auth_headers
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Seated"

    def test_update_position_authorized(
        self, client: TestClient, auth_headers, position: Position
    ):
        """Test updating position with authentication."""
        update_data = {"name": "Updated Position"}
        response = client.put(
            f"/api/v1/exercises/positions/{position.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Position"

    def test_delete_position_authorized(
        self, client: TestClient, auth_headers, position: Position
    ):
        """Test deleting position with authentication."""
        response = client.delete(
            f"/api/v1/exercises/positions/{position.id}", headers=auth_headers
        )
        assert response.status_code == 204


class TestContractionTypeEndpoints:
    """Test suite for contraction type endpoints."""

    def test_read_contraction_types_empty(self, client: TestClient):
        """Test reading contraction types when database is empty."""
        response = client.get("/api/v1/exercises/contraction-types/")
        assert response.status_code == 200
        data = response.json()
        assert data["contraction_types"] == []
        assert data["total"] == 0

    def test_read_contraction_types_with_data(
        self, client: TestClient, contraction_type: ContractionType
    ):
        """Test reading contraction types with existing data."""
        response = client.get("/api/v1/exercises/contraction-types/")
        assert response.status_code == 200
        data = response.json()
        assert len(data["contraction_types"]) == 1
        assert data["total"] == 1
        assert data["contraction_types"][0]["name"] == "Concentric"

    def test_create_contraction_type_authorized(self, client: TestClient, auth_headers):
        """Test creating contraction type with authentication."""
        contraction_type_data = {"name": "Eccentric"}
        response = client.post(
            "/api/v1/exercises/contraction-types/",
            json=contraction_type_data,
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["name"] == "Eccentric"

    def test_update_contraction_type_authorized(
        self, client: TestClient, auth_headers, contraction_type: ContractionType
    ):
        """Test updating contraction type with authentication."""
        update_data = {"name": "Updated Contraction Type"}
        response = client.put(
            f"/api/v1/exercises/contraction-types/{contraction_type.id}",
            json=update_data,
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Updated Contraction Type"

    def test_delete_contraction_type_authorized(
        self, client: TestClient, auth_headers, contraction_type: ContractionType
    ):
        """Test deleting contraction type with authentication."""
        response = client.delete(
            f"/api/v1/exercises/contraction-types/{contraction_type.id}",
            headers=auth_headers,
        )
        assert response.status_code == 204

    def test_pagination_categories(
        self, client: TestClient, auth_headers, db_session: Session
    ):
        """Test pagination for categories."""
        # Create multiple categories
        for i in range(15):
            category = ExerciseCategory(name=f"Category {i}")
            db_session.add(category)
        db_session.commit()

        # Test first page
        response = client.get("/api/v1/exercises/categories/?skip=0&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 10
        assert data["total"] == 15

        # Test second page
        response = client.get("/api/v1/exercises/categories/?skip=10&limit=10")
        assert response.status_code == 200
        data = response.json()
        assert len(data["categories"]) == 5
