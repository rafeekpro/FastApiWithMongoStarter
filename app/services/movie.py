import logging
from typing import List, Optional

from app.core.exceptions import NotFoundException
from app.repositories.movie import MovieRepository
from app.schemas.movie import Movie, MovieCreate, MovieFilters, MovieUpdate

logger = logging.getLogger(__name__)


class MovieService:
    """Service layer for movie operations."""

    def __init__(self, repository: MovieRepository):
        self.repository = repository

    async def create_movie(self, movie: MovieCreate) -> Movie:
        """Create a new movie."""
        movie_in_db = await self.repository.create(movie)
        return self._to_schema(movie_in_db)

    async def get_movie(self, movie_id: str) -> Movie:
        """Get a movie by ID."""
        movie_in_db = await self.repository.get_by_id(movie_id)

        if not movie_in_db:
            raise NotFoundException(f"Movie with id {movie_id} not found")

        return self._to_schema(movie_in_db)

    async def get_movie_by_slug(self, slug: str) -> Movie:
        """Get a movie by slug."""
        movie_in_db = await self.repository.get_by_slug(slug)

        if not movie_in_db:
            raise NotFoundException(f"Movie with slug {slug} not found")

        return self._to_schema(movie_in_db)

    async def get_movies(self, filters: MovieFilters) -> tuple[List[Movie], int]:
        """Get movies with filters and total count."""
        movies_in_db = await self.repository.get_many(filters)
        total_count = await self.repository.count(filters)

        movies = [self._to_schema(movie) for movie in movies_in_db]
        return movies, total_count

    async def update_movie(self, movie_id: str, movie_update: MovieUpdate) -> Movie:
        """Update a movie."""
        movie_in_db = await self.repository.update(movie_id, movie_update)

        if not movie_in_db:
            raise NotFoundException(f"Movie with id {movie_id} not found")

        return self._to_schema(movie_in_db)

    async def delete_movie(self, movie_id: str) -> bool:
        """Delete a movie."""
        deleted = await self.repository.delete(movie_id)

        if not deleted:
            raise NotFoundException(f"Movie with id {movie_id} not found")

        return True

    def _to_schema(self, movie_in_db) -> Movie:
        """Convert MovieInDB to Movie schema."""
        movie_dict = movie_in_db.model_dump(by_alias=True)
        movie_dict["id"] = movie_dict.pop("_id")
        return Movie(**movie_dict)
