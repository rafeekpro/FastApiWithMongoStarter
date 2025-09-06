"""Unit tests for service layer."""

import pytest
from unittest.mock import AsyncMock, MagicMock
from datetime import datetime

from app.services.movie import MovieService
from app.repositories.movie import MovieRepository
from app.schemas.movie import MovieCreate, MovieFilters, MovieUpdate, MovieInDB
from app.core.exceptions import NotFoundException


@pytest.fixture
def mock_repository():
    """Create a mock repository."""
    return MagicMock(spec=MovieRepository)


@pytest.fixture
def service(mock_repository):
    """Create a service with mock repository."""
    return MovieService(mock_repository)


class TestMovieService:
    """Test movie service operations."""

    @pytest.mark.asyncio
    async def test_create_movie(self, service, mock_repository):
        """Test creating a movie through service."""
        movie_data = MovieCreate(
            name="Test Movie",
            casts=["Actor 1"],
            genres=["Action"],
            year=2024
        )
        
        mock_movie_in_db = MovieInDB(
            _id="507f1f77bcf86cd799439011",
            name="Test Movie",
            slug="test-movie",
            casts=["Actor 1"],
            genres=["Action"],
            year=2024,
            classification=[],
            createdAt=datetime.utcnow(),
            updatedAt=None
        )
        
        mock_repository.create = AsyncMock(return_value=mock_movie_in_db)
        
        result = await service.create_movie(movie_data)
        
        assert result.name == "Test Movie"
        assert result.slug == "test-movie"
        mock_repository.create.assert_called_once_with(movie_data)

    @pytest.mark.asyncio
    async def test_get_movie_found(self, service, mock_repository):
        """Test getting a movie when found."""
        movie_id = "507f1f77bcf86cd799439011"
        
        mock_movie_in_db = MovieInDB(
            _id=movie_id,
            name="Test Movie",
            slug="test-movie",
            casts=[],
            genres=[],
            year=2024,
            classification=[],
            createdAt=datetime.utcnow(),
            updatedAt=None
        )
        
        mock_repository.get_by_id = AsyncMock(return_value=mock_movie_in_db)
        
        result = await service.get_movie(movie_id)
        
        assert result.id == movie_id
        assert result.name == "Test Movie"

    @pytest.mark.asyncio
    async def test_get_movie_not_found(self, service, mock_repository):
        """Test getting a movie when not found."""
        movie_id = "507f1f77bcf86cd799439011"
        
        mock_repository.get_by_id = AsyncMock(return_value=None)
        
        with pytest.raises(NotFoundException) as exc_info:
            await service.get_movie(movie_id)
        
        assert f"Movie with id {movie_id} not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_movie_by_slug_found(self, service, mock_repository):
        """Test getting a movie by slug when found."""
        slug = "test-movie"
        
        mock_movie_in_db = MovieInDB(
            _id="507f1f77bcf86cd799439011",
            name="Test Movie",
            slug=slug,
            casts=[],
            genres=[],
            year=2024,
            classification=[],
            createdAt=datetime.utcnow(),
            updatedAt=None
        )
        
        mock_repository.get_by_slug = AsyncMock(return_value=mock_movie_in_db)
        
        result = await service.get_movie_by_slug(slug)
        
        assert result.slug == slug
        assert result.name == "Test Movie"

    @pytest.mark.asyncio
    async def test_get_movie_by_slug_not_found(self, service, mock_repository):
        """Test getting a movie by slug when not found."""
        slug = "non-existent"
        
        mock_repository.get_by_slug = AsyncMock(return_value=None)
        
        with pytest.raises(NotFoundException) as exc_info:
            await service.get_movie_by_slug(slug)
        
        assert f"Movie with slug {slug} not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_get_movies_with_filters(self, service, mock_repository):
        """Test getting movies with filters."""
        filters = MovieFilters(title="Test", limit=10)
        
        mock_movies = [
            MovieInDB(
                _id="507f1f77bcf86cd799439011",
                name="Test Movie 1",
                slug="test-movie-1",
                casts=[],
                genres=[],
                year=2024,
                classification=[],
                createdAt=datetime.utcnow(),
                updatedAt=None
            ),
            MovieInDB(
                _id="507f1f77bcf86cd799439012",
                name="Test Movie 2",
                slug="test-movie-2",
                casts=[],
                genres=[],
                year=2023,
                classification=[],
                createdAt=datetime.utcnow(),
                updatedAt=None
            )
        ]
        
        mock_repository.get_many = AsyncMock(return_value=mock_movies)
        mock_repository.count = AsyncMock(return_value=2)
        
        movies, count = await service.get_movies(filters)
        
        assert len(movies) == 2
        assert count == 2
        assert movies[0].name == "Test Movie 1"
        assert movies[1].name == "Test Movie 2"

    @pytest.mark.asyncio
    async def test_update_movie_found(self, service, mock_repository):
        """Test updating a movie when found."""
        movie_id = "507f1f77bcf86cd799439011"
        update_data = MovieUpdate(name="Updated Movie")
        
        mock_movie_in_db = MovieInDB(
            _id=movie_id,
            name="Updated Movie",
            slug="updated-movie",
            casts=[],
            genres=[],
            year=2024,
            classification=[],
            createdAt=datetime.utcnow(),
            updatedAt=datetime.utcnow()
        )
        
        mock_repository.update = AsyncMock(return_value=mock_movie_in_db)
        
        result = await service.update_movie(movie_id, update_data)
        
        assert result.name == "Updated Movie"
        assert result.slug == "updated-movie"

    @pytest.mark.asyncio
    async def test_update_movie_not_found(self, service, mock_repository):
        """Test updating a movie when not found."""
        movie_id = "507f1f77bcf86cd799439011"
        update_data = MovieUpdate(name="Updated Movie")
        
        mock_repository.update = AsyncMock(return_value=None)
        
        with pytest.raises(NotFoundException) as exc_info:
            await service.update_movie(movie_id, update_data)
        
        assert f"Movie with id {movie_id} not found" in str(exc_info.value.detail)

    @pytest.mark.asyncio
    async def test_delete_movie_success(self, service, mock_repository):
        """Test deleting a movie successfully."""
        movie_id = "507f1f77bcf86cd799439011"
        
        mock_repository.delete = AsyncMock(return_value=True)
        
        result = await service.delete_movie(movie_id)
        
        assert result is True

    @pytest.mark.asyncio
    async def test_delete_movie_not_found(self, service, mock_repository):
        """Test deleting a movie when not found."""
        movie_id = "507f1f77bcf86cd799439011"
        
        mock_repository.delete = AsyncMock(return_value=False)
        
        with pytest.raises(NotFoundException) as exc_info:
            await service.delete_movie(movie_id)
        
        assert f"Movie with id {movie_id} not found" in str(exc_info.value.detail)