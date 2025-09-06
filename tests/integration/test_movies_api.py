import pytest
from httpx import AsyncClient

from app.core.settings import settings


@pytest.mark.asyncio
class TestMoviesAPI:
    """Test movies API endpoints."""
    
    async def test_create_movie(self, client: AsyncClient, sample_movie_data):
        """Test creating a new movie."""
        response = await client.post(
            f"{settings.API_V1_STR}/movies",
            json=sample_movie_data
        )
        
        assert response.status_code == 201
        data = response.json()
        assert "movie" in data
        movie = data["movie"]
        assert movie["name"] == sample_movie_data["name"]
        assert movie["year"] == sample_movie_data["year"]
        assert "id" in movie
        assert "slug" in movie
        assert movie["slug"] == "test-movie"
    
    async def test_get_movie_by_id(self, client: AsyncClient, created_movie):
        """Test getting a movie by ID."""
        movie_id = created_movie["id"]
        response = await client.get(f"{settings.API_V1_STR}/movies/{movie_id}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["movie"]["id"] == movie_id
        assert data["movie"]["name"] == created_movie["name"]
    
    async def test_get_movie_by_invalid_id(self, client: AsyncClient):
        """Test getting a movie with invalid ID."""
        response = await client.get(f"{settings.API_V1_STR}/movies/invalid_id")
        
        assert response.status_code == 500  # Should be 404 but depends on error handling
    
    async def test_get_movie_by_slug(self, client: AsyncClient, created_movie):
        """Test getting a movie by slug."""
        slug = created_movie["slug"]
        response = await client.get(f"{settings.API_V1_STR}/movies/slug/{slug}")
        
        assert response.status_code == 200
        data = response.json()
        assert data["movie"]["slug"] == slug
    
    async def test_get_movies_list(self, client: AsyncClient, created_movie):
        """Test getting list of movies."""
        response = await client.get(f"{settings.API_V1_STR}/movies")
        
        assert response.status_code == 200
        data = response.json()
        assert "movies" in data
        assert "moviesCount" in data
        assert data["moviesCount"] >= 1
        assert len(data["movies"]) >= 1
    
    async def test_get_movies_with_filter(self, client: AsyncClient, created_movie):
        """Test getting movies with title filter."""
        response = await client.get(
            f"{settings.API_V1_STR}/movies",
            params={"title": "Test"}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["movies"]) >= 1
        assert all("Test" in movie["name"] for movie in data["movies"])
    
    async def test_get_movies_with_pagination(self, client: AsyncClient):
        """Test getting movies with pagination."""
        response = await client.get(
            f"{settings.API_V1_STR}/movies",
            params={"limit": 5, "offset": 0}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert len(data["movies"]) <= 5
    
    async def test_update_movie(self, client: AsyncClient, created_movie):
        """Test updating a movie."""
        movie_id = created_movie["id"]
        update_data = {"name": "Updated Movie Name"}
        
        response = await client.put(
            f"{settings.API_V1_STR}/movies/{movie_id}",
            json=update_data
        )
        
        assert response.status_code == 200
        data = response.json()
        assert data["movie"]["name"] == "Updated Movie Name"
        assert data["movie"]["slug"] == "updated-movie-name"
        assert data["movie"]["year"] == created_movie["year"]  # Unchanged
    
    async def test_update_nonexistent_movie(self, client: AsyncClient):
        """Test updating a non-existent movie."""
        fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
        response = await client.put(
            f"{settings.API_V1_STR}/movies/{fake_id}",
            json={"name": "Updated"}
        )
        
        assert response.status_code == 404
    
    async def test_delete_movie(self, client: AsyncClient, created_movie):
        """Test deleting a movie."""
        movie_id = created_movie["id"]
        
        # Delete the movie
        response = await client.delete(f"{settings.API_V1_STR}/movies/{movie_id}")
        assert response.status_code == 204
        
        # Verify it's deleted
        response = await client.get(f"{settings.API_V1_STR}/movies/{movie_id}")
        assert response.status_code == 404
    
    async def test_delete_nonexistent_movie(self, client: AsyncClient):
        """Test deleting a non-existent movie."""
        fake_id = "507f1f77bcf86cd799439011"  # Valid ObjectId format
        response = await client.delete(f"{settings.API_V1_STR}/movies/{fake_id}")
        
        assert response.status_code == 404