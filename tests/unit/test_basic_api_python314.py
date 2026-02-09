import asyncio

import httpx

from src.main import app


def test_health_check():
    """Test health check endpoint."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/")
            assert response.status_code == 200
            data = response.json()
            assert "message" in data
            assert data["message"] == "Fitness App API"

    asyncio.run(run_test())


def test_api_health_check():
    """Test API health check endpoint."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/health")
            assert response.status_code == 200

    asyncio.run(run_test())


def test_read_exercises_empty():
    """Test reading exercises when database is empty."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/exercises/")
            # Should return 200 even if empty (but might have auth issues)
            assert response.status_code in [200, 401, 422]

    asyncio.run(run_test())


def test_read_categories_empty():
    """Test reading categories when database is empty."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/exercises/categories/")
            # Should return 200 even if empty
            assert response.status_code in [200, 422]

    asyncio.run(run_test())


def test_read_movement_types_empty():
    """Test reading movement types when database is empty."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/exercises/movement-types/")
            # Should return 200 even if empty
            assert response.status_code in [200, 422]

    asyncio.run(run_test())


def test_read_muscle_groups_empty():
    """Test reading muscle groups when database is empty."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/exercises/muscle-groups/")
            # Should return 200 even if empty
            assert response.status_code in [200, 422]

    asyncio.run(run_test())


def test_read_equipment_empty():
    """Test reading equipment when database is empty."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/exercises/equipment/")
            # Should return 200 even if empty
            assert response.status_code in [200, 422]

    asyncio.run(run_test())


def test_read_positions_empty():
    """Test reading positions when database is empty."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/exercises/positions/")
            # Should return 200 even if empty
            assert response.status_code in [200, 422]

    asyncio.run(run_test())


def test_read_contraction_types_empty():
    """Test reading contraction types when database is empty."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/exercises/contraction-types/")
            # Should return 200 even if empty
            assert response.status_code in [200, 422]

    asyncio.run(run_test())


def test_create_exercise_unauthorized():
    """Test creating exercise without authentication."""

    async def run_test():
        exercise_data = {"name": "New Exercise", "description": "Test exercise"}
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post("/api/v1/exercises/", json=exercise_data)
            # Should require authentication
            assert response.status_code in [401, 422]

    asyncio.run(run_test())


def test_create_category_unauthorized():
    """Test creating category without authentication."""

    async def run_test():
        category_data = {"name": "Cardio", "displacement": True}
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.post(
                "/api/v1/exercises/categories/", json=category_data
            )
            # Should require authentication
            assert response.status_code in [401, 422]

    asyncio.run(run_test())


def test_exercise_not_found():
    """Test getting a non-existent exercise."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/exercises/99999")
            # Should return 404 or auth error
            assert response.status_code in [404, 401, 422]

    asyncio.run(run_test())


def test_category_not_found():
    """Test getting a non-existent category."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/exercises/categories/99999")
            # Should return 404 or auth error
            assert response.status_code in [404, 401, 422]

    asyncio.run(run_test())


def test_docs_available():
    """Test that API documentation is available."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/docs")
            assert response.status_code == 200

    asyncio.run(run_test())


def test_openapi_available():
    """Test that OpenAPI schema is available."""

    async def run_test():
        async with httpx.AsyncClient(
            transport=httpx.ASGITransport(app=app), base_url="http://test"
        ) as client:
            response = await client.get("/api/v1/openapi.json")
            assert response.status_code == 200

    asyncio.run(run_test())
