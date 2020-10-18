from typing import List, Optional
from bson import ObjectId
from slugify import slugify
from datetime import datetime

from ..models.movie import (
    MovieFilterParams,
    MovieInDB,
)
from ..db.mongodb import AsyncIOMotorClient
from ..core.config import database_name, movie_collection


async def get_movies_with_filters(
    conn: AsyncIOMotorClient, filters: MovieFilterParams
) -> List[MovieInDB]:
    movies: List[MovieInDB] = []
    base_query = {}

    if filters.title:
        movies = filters.title.replace(", ", ",").split(',')
        base_query["Movie"] = { "$in": movies }


    rows = conn[database_name][movie_collection].find(base_query,
                                                                limit=filters.limit,
                                                                skip=filters.offset)
    async for row in rows:
        # slug = row["slug"]
        # author = await get_profile_for_user(conn, row["author_id"], username)
        # tags = await get_tags_for_article(conn, slug)
        # favorites_count = await get_favorites_count_for_article(conn, slug)
        # favorited_by_user = await is_article_favorited_by_user(conn, slug, username)
        movies.append(
            MovieInDB(
                **row,
                created_at=ObjectId(row["_id"]).generation_time,
            )
        )
    return movies
