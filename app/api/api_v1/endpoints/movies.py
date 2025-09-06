from typing import Annotated

from fastapi import APIRouter, Depends, Query, status

from app.api.deps import get_movie_service
from app.schemas.movie import (
    Movie,
    MovieCreate,
    MovieFilters,
    MovieResponse,
    MoviesResponse,
    MovieUpdate,
)
from app.services.movie import MovieService

router = APIRouter()


@router.get("/movies", response_model=MoviesResponse, tags=["movies"])
async def get_movies(
    title: Annotated[str, Query(description="Filter by title")] = "",
    limit: Annotated[int, Query(ge=1, le=100)] = 20,
    offset: Annotated[int, Query(ge=0)] = 0,
    service: MovieService = Depends(get_movie_service),
) -> MoviesResponse:
    """Get list of movies with optional filters."""
    filters = MovieFilters(title=title or None, limit=limit, offset=offset)
    movies, total_count = await service.get_movies(filters)

    return MoviesResponse(movies=movies, moviesCount=total_count)


@router.get("/movies/{movie_id}", response_model=MovieResponse, tags=["movies"])
async def get_movie(
    movie_id: str,
    service: MovieService = Depends(get_movie_service),
) -> MovieResponse:
    """Get a single movie by ID."""
    movie = await service.get_movie(movie_id)
    return MovieResponse(movie=movie)


@router.get("/movies/slug/{slug}", response_model=MovieResponse, tags=["movies"])
async def get_movie_by_slug(
    slug: str,
    service: MovieService = Depends(get_movie_service),
) -> MovieResponse:
    """Get a single movie by slug."""
    movie = await service.get_movie_by_slug(slug)
    return MovieResponse(movie=movie)


@router.post(
    "/movies",
    response_model=MovieResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["movies"],
)
async def create_movie(
    movie: MovieCreate,
    service: MovieService = Depends(get_movie_service),
) -> MovieResponse:
    """Create a new movie."""
    created_movie = await service.create_movie(movie)
    return MovieResponse(movie=created_movie)


@router.put("/movies/{movie_id}", response_model=MovieResponse, tags=["movies"])
async def update_movie(
    movie_id: str,
    movie_update: MovieUpdate,
    service: MovieService = Depends(get_movie_service),
) -> MovieResponse:
    """Update a movie."""
    updated_movie = await service.update_movie(movie_id, movie_update)
    return MovieResponse(movie=updated_movie)


@router.delete(
    "/movies/{movie_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["movies"],
)
async def delete_movie(
    movie_id: str,
    service: MovieService = Depends(get_movie_service),
) -> None:
    """Delete a movie."""
    await service.delete_movie(movie_id)
