import asyncio
from typing import AsyncGenerator, Generator

import pytest
from httpx import AsyncClient
from motor.motor_asyncio import AsyncIOMotorClient

from app.core.settings import settings
from app.db.database import db
from app.main import app


@pytest.fixture(scope="session")
def event_loop() -> Generator:
    """Create an instance of the default event loop for the test session."""
    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture
async def test_db() -> AsyncGenerator:
    """Create a test database connection."""
    # Use a test database
    test_db_name = f"{settings.MONGO_DB}_test"
    
    # Create test client
    client = AsyncIOMotorClient(settings.MONGODB_URL)
    test_database = client[test_db_name]
    
    # Set the test database in the app
    db.client = client
    db.database = test_database
    
    yield test_database
    
    # Cleanup: Drop test database
    await client.drop_database(test_db_name)
    client.close()


@pytest.fixture
async def client(test_db) -> AsyncGenerator:
    """Create a test client for the FastAPI app."""
    async with AsyncClient(app=app, base_url="http://test") as ac:
        yield ac


@pytest.fixture
async def sample_movie_data():
    """Provide sample movie data for tests."""
    return {
        "name": "Test Movie",
        "casts": ["Actor 1", "Actor 2"],
        "genres": ["Action", "Drama"],
        "year": 2024
    }


@pytest.fixture
async def created_movie(client: AsyncClient, sample_movie_data):
    """Create a movie and return it."""
    response = await client.post(
        f"{settings.API_V1_STR}/movies",
        json=sample_movie_data
    )
    assert response.status_code == 201
    return response.json()["movie"]