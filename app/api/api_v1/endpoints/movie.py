from typing import Optional
from fastapi import APIRouter, Body, Depends, Path, Query
from slugify import slugify
from starlette.exceptions import HTTPException
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)

from ....core.utils import create_aliased_response
from ....crud.movie import (
    get_movies_with_filters,
)
# from ....crud.shortcuts import (
#     get_scoreboard_or_404,
# )
from ....db.mongodb import AsyncIOMotorClient, get_database
from ....models.movie import (
    MovieFilterParams,
    MovieInResponse,
    ManyMoviesInResponse
)

router = APIRouter()


@router.get("/movies", response_model=ManyMoviesInResponse, tags=["elements"])
async def get_articles(
        title: str = "",
        limit: int = Query(20, gt=0),
        offset: int = Query(0, ge=0),
        # user: User = Depends(get_current_user_authorizer(required=False)),
        db: AsyncIOMotorClient = Depends(get_database),
):
    filters = MovieFilterParams(
        movie=title, limit=limit, offset=offset
    )
    dbmovies = await get_movies_with_filters(
        db, filters
    )
    return create_aliased_response(
        ManyMoviesInResponse(movies=dbmovies, movies_count=len(dbmovies))
        # ManyScoreboardsInResponse(scoreboards=dbscoreboards)
    )
