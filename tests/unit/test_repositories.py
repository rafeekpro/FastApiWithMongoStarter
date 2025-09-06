"""Unit tests for repository layer."""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch
from datetime import datetime
from bson import ObjectId

from app.repositories.movie import MovieRepository
from app.schemas.movie import MovieCreate, MovieFilters, MovieUpdate
from app.core.exceptions import DatabaseException


@pytest.fixture
def mock_db():
    """Create a mock database."""
    mock = MagicMock()
    mock.__getitem__ = MagicMock(return_value=MagicMock())
    return mock


@pytest.fixture
def repository(mock_db):
    """Create a repository with mock database."""
    return MovieRepository(mock_db)


class TestMovieRepository:
    """Test movie repository operations."""

    @pytest.mark.asyncio
    async def test_create_movie_success(self, repository):
        """Test successful movie creation."""
        movie_data = MovieCreate(
            name="Test Movie",
            casts=["Actor 1"],
            genres=["Action"],
            year=2024
        )
        
        mock_insert_result = MagicMock()
        mock_insert_result.inserted_id = ObjectId()
        
        repository.collection.insert_one = AsyncMock(return_value=mock_insert_result)
        repository.collection.find_one = AsyncMock(return_value={
            "_id": str(mock_insert_result.inserted_id),
            "name": "Test Movie",
            "slug": "test-movie",
            "casts": ["Actor 1"],
            "genres": ["Action"],
            "year": 2024,
            "classification": [],
            "created_at": datetime.utcnow()
        })
        
        result = await repository.create(movie_data)
        
        assert result.name == "Test Movie"
        assert result.slug == "test-movie"
        repository.collection.insert_one.assert_called_once()

    @pytest.mark.asyncio
    async def test_create_movie_failure(self, repository):
        """Test movie creation failure."""
        movie_data = MovieCreate(
            name="Test Movie",
            casts=[],
            genres=[],
            year=2024
        )
        
        repository.collection.insert_one = AsyncMock(side_effect=Exception("DB Error"))
        
        with pytest.raises(DatabaseException):
            await repository.create(movie_data)

    @pytest.mark.asyncio
    async def test_get_by_id_found(self, repository):
        """Test getting movie by ID when found."""
        movie_id = str(ObjectId())
        repository.collection.find_one = AsyncMock(return_value={
            "_id": movie_id,
            "name": "Test Movie",
            "slug": "test-movie",
            "year": 2024
        })
        
        result = await repository.get_by_id(movie_id)
        
        assert result is not None
        assert result.name == "Test Movie"

    @pytest.mark.asyncio
    async def test_get_by_id_not_found(self, repository):
        """Test getting movie by ID when not found."""
        movie_id = str(ObjectId())
        repository.collection.find_one = AsyncMock(return_value=None)
        
        result = await repository.get_by_id(movie_id)
        
        assert result is None

    @pytest.mark.asyncio
    async def test_get_by_id_invalid(self, repository):
        """Test getting movie with invalid ID."""
        result = await repository.get_by_id("invalid_id")
        assert result is None

    @pytest.mark.asyncio
    async def test_get_many_with_filters(self, repository):
        """Test getting movies with filters."""
        filters = MovieFilters(title="Test", limit=10, offset=0)
        
        mock_cursor = AsyncMock()
        mock_cursor.skip.return_value = mock_cursor
        mock_cursor.limit.return_value = mock_cursor
        mock_cursor.__aiter__.return_value = [
            {
                "_id": str(ObjectId()),
                "name": "Test Movie 1",
                "slug": "test-movie-1",
                "year": 2024
            },
            {
                "_id": str(ObjectId()),
                "name": "Test Movie 2",
                "slug": "test-movie-2",
                "year": 2023
            }
        ].__iter__()
        
        repository.collection.find = AsyncMock(return_value=mock_cursor)
        
        result = await repository.get_many(filters)
        
        assert len(result) == 2
        assert result[0].name == "Test Movie 1"
        assert result[1].name == "Test Movie 2"

    @pytest.mark.asyncio
    async def test_update_movie_success(self, repository):
        """Test successful movie update."""
        movie_id = str(ObjectId())
        update_data = MovieUpdate(name="Updated Movie")
        
        repository.collection.find_one_and_update = AsyncMock(return_value={
            "_id": movie_id,
            "name": "Updated Movie",
            "slug": "updated-movie",
            "year": 2024,
            "updated_at": datetime.utcnow()
        })
        
        result = await repository.update(movie_id, update_data)
        
        assert result is not None
        assert result.name == "Updated Movie"
        assert result.slug == "updated-movie"

    @pytest.mark.asyncio
    async def test_update_movie_not_found(self, repository):
        """Test updating non-existent movie."""
        movie_id = str(ObjectId())
        update_data = MovieUpdate(name="Updated Movie")
        
        repository.collection.find_one_and_update = AsyncMock(return_value=None)
        
        result = await repository.update(movie_id, update_data)
        
        assert result is None

    @pytest.mark.asyncio
    async def test_delete_movie_success(self, repository):
        """Test successful movie deletion."""
        movie_id = str(ObjectId())
        
        mock_result = MagicMock()
        mock_result.deleted_count = 1
        repository.collection.delete_one = AsyncMock(return_value=mock_result)
        
        result = await repository.delete(movie_id)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_movie_not_found(self, repository):
        """Test deleting non-existent movie."""
        movie_id = str(ObjectId())
        
        mock_result = MagicMock()
        mock_result.deleted_count = 0
        repository.collection.delete_one = AsyncMock(return_value=mock_result)
        
        result = await repository.delete(movie_id)
        
        assert result is False

    @pytest.mark.asyncio
    async def test_count_with_filters(self, repository):
        """Test counting movies with filters."""
        filters = MovieFilters(genres=["Action"])
        
        repository.collection.count_documents = AsyncMock(return_value=5)
        
        result = await repository.count(filters)
        
        assert result == 5
        repository.collection.count_documents.assert_called_once()