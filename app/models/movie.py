from typing import List
from datetime import datetime

from pydantic import Field
from .dbmodel import DateTimeModelMixin, DBModelMixin
from .rwmodel import RWModel
from .classification import Classification


class MovieFilterParams(RWModel):
    title: str = ""
    limit: int = 20
    offset: int = 0


class MovieBase(RWModel):
    name: str = ""
    casts: List[str] = []
    genres: List[str] = []
    year: int = 0


# Add Datetime created/updates information
# and slug and classification
class Movie(DateTimeModelMixin, MovieBase):
    slug: str
    classification: List[Classification]


# Add Id information
class MovieInDB(DBModelMixin, Movie):
    pass


class MovieInResponse(RWModel):
    movie: Movie


class ManyMoviesInResponse(RWModel):
    movies: List[Movie]
    movies_count: int = Field(..., alias="moviesCount")
