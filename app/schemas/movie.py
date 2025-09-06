from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, field_validator


class ClassificationSchema(BaseModel):
    country: str = Field(default="", description="Country code")
    value: str = Field(default="", description="Classification value")


class MovieBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200, description="Movie title")
    casts: List[str] = Field(default=[], description="List of cast members")
    genres: List[str] = Field(default=[], description="List of genres")
    year: int = Field(..., ge=1900, le=2100, description="Release year")

    @field_validator("name")
    @classmethod
    def validate_name(cls, v: str) -> str:
        return v.strip()

    @field_validator("casts", "genres")
    @classmethod
    def validate_list_items(cls, v: List[str]) -> List[str]:
        return [item.strip() for item in v if item.strip()]


class MovieCreate(MovieBase):
    """Schema for creating a movie."""

    pass


class MovieUpdate(BaseModel):
    """Schema for updating a movie."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    casts: Optional[List[str]] = None
    genres: Optional[List[str]] = None
    year: Optional[int] = Field(None, ge=1900, le=2100)


class MovieInDB(MovieBase):
    """Schema for movie in database."""

    id: str = Field(..., alias="_id")
    slug: str
    classification: List[ClassificationSchema] = []
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True, "json_encoders": {datetime: lambda v: v.isoformat() if v else None}}


class Movie(MovieBase):
    """Schema for movie response."""

    id: str
    slug: str
    classification: List[ClassificationSchema] = []
    created_at: datetime = Field(..., alias="createdAt")
    updated_at: Optional[datetime] = Field(None, alias="updatedAt")

    model_config = {"populate_by_name": True, "json_encoders": {datetime: lambda v: v.isoformat() if v else None}}


class MovieResponse(BaseModel):
    """Single movie response."""

    movie: Movie


class MoviesResponse(BaseModel):
    """Multiple movies response."""

    movies: List[Movie]
    movies_count: int = Field(..., alias="moviesCount")

    model_config = {"populate_by_name": True}


class MovieFilters(BaseModel):
    """Filters for movie queries."""

    title: Optional[str] = Field(None, description="Filter by title (partial match)")
    genres: Optional[List[str]] = Field(None, description="Filter by genres")
    year_min: Optional[int] = Field(None, ge=1900, description="Minimum year")
    year_max: Optional[int] = Field(None, le=2100, description="Maximum year")
    limit: int = Field(20, ge=1, le=100, description="Number of results")
    offset: int = Field(0, ge=0, description="Offset for pagination")
