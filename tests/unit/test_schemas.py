import pytest
from pydantic import ValidationError

from app.schemas.movie import MovieCreate, MovieFilters, MovieUpdate


class TestMovieSchemas:
    """Test movie schemas validation."""

    def test_movie_create_valid(self):
        """Test creating a valid movie."""
        movie = MovieCreate(name="Test Movie", casts=["Actor 1", "Actor 2"], genres=["Action"], year=2024)
        assert movie.name == "Test Movie"
        assert len(movie.casts) == 2
        assert movie.year == 2024

    def test_movie_create_strips_whitespace(self):
        """Test that movie name is stripped of whitespace."""
        movie = MovieCreate(name="  Test Movie  ", casts=["  Actor 1  ", "Actor 2"], genres=["Action"], year=2024)
        assert movie.name == "Test Movie"
        assert movie.casts[0] == "Actor 1"

    def test_movie_create_invalid_year(self):
        """Test that invalid year raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            MovieCreate(name="Test Movie", casts=[], genres=[], year=1800)  # Too old
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("year",) for error in errors)

    def test_movie_create_empty_name(self):
        """Test that empty name raises validation error."""
        with pytest.raises(ValidationError) as exc_info:
            MovieCreate(name="", casts=[], genres=[], year=2024)
        errors = exc_info.value.errors()
        assert any(error["loc"] == ("name",) for error in errors)

    def test_movie_update_partial(self):
        """Test partial movie update."""
        update = MovieUpdate(name="Updated Name")
        assert update.name == "Updated Name"
        assert update.year is None
        assert update.casts is None

    def test_movie_filters_defaults(self):
        """Test movie filters with default values."""
        filters = MovieFilters()
        assert filters.limit == 20
        assert filters.offset == 0
        assert filters.title is None

    def test_movie_filters_validation(self):
        """Test movie filters validation."""
        with pytest.raises(ValidationError) as exc_info:
            MovieFilters(limit=150)  # Exceeds max limit

        errors = exc_info.value.errors()
        assert any(error["loc"] == ("limit",) for error in errors)
