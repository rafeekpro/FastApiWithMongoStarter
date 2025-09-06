from typing import Annotated

from fastapi import Depends

from app.db.database import get_database
from app.repositories.movie import MovieRepository
from app.services.movie import MovieService


async def get_movie_repository() -> MovieRepository:
    """Get movie repository instance."""
    db = get_database()
    return MovieRepository(db)


async def get_movie_service(
    repository: Annotated[MovieRepository, Depends(get_movie_repository)]
) -> MovieService:
    """Get movie service instance."""
    return MovieService(repository)