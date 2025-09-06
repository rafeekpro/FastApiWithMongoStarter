import logging
from datetime import datetime
from typing import List, Optional

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo import ReturnDocument
from slugify import slugify

from app.core.exceptions import DatabaseException, NotFoundException
from app.core.settings import settings
from app.schemas.movie import MovieCreate, MovieFilters, MovieInDB, MovieUpdate

logger = logging.getLogger(__name__)


class MovieRepository:
    """Repository for movie database operations."""

    def __init__(self, db: AsyncIOMotorDatabase):
        self.db = db
        self.collection = db[settings.MOVIE_COLLECTION]

    async def create(self, movie: MovieCreate) -> MovieInDB:
        """Create a new movie."""
        try:
            movie_dict = movie.model_dump()
            movie_dict["slug"] = slugify(movie.name)
            movie_dict["classification"] = []
            movie_dict["created_at"] = datetime.utcnow()
            movie_dict["updated_at"] = None

            result = await self.collection.insert_one(movie_dict)

            if not result.inserted_id:
                raise DatabaseException("Failed to create movie")

            created_movie = await self.collection.find_one({"_id": result.inserted_id})
            return MovieInDB(**self._prepare_movie(created_movie))

        except Exception as e:
            logger.error(f"Error creating movie: {e}")
            raise DatabaseException(f"Failed to create movie: {str(e)}")

    async def get_by_id(self, movie_id: str) -> Optional[MovieInDB]:
        """Get movie by ID."""
        try:
            if not ObjectId.is_valid(movie_id):
                return None

            movie = await self.collection.find_one({"_id": ObjectId(movie_id)})

            if not movie:
                return None

            return MovieInDB(**self._prepare_movie(movie))

        except Exception as e:
            logger.error(f"Error getting movie by id {movie_id}: {e}")
            raise DatabaseException(f"Failed to get movie: {str(e)}")

    async def get_by_slug(self, slug: str) -> Optional[MovieInDB]:
        """Get movie by slug."""
        try:
            movie = await self.collection.find_one({"slug": slug})

            if not movie:
                return None

            return MovieInDB(**self._prepare_movie(movie))

        except Exception as e:
            logger.error(f"Error getting movie by slug {slug}: {e}")
            raise DatabaseException(f"Failed to get movie: {str(e)}")

    async def get_many(self, filters: MovieFilters) -> List[MovieInDB]:
        """Get movies with filters."""
        try:
            query = {}

            # Build query based on filters
            if filters.title:
                query["name"] = {"$regex": filters.title, "$options": "i"}

            if filters.genres:
                query["genres"] = {"$in": filters.genres}

            if filters.year_min or filters.year_max:
                year_query = {}
                if filters.year_min:
                    year_query["$gte"] = filters.year_min
                if filters.year_max:
                    year_query["$lte"] = filters.year_max
                query["year"] = year_query

            # Execute query with pagination
            cursor = self.collection.find(query).skip(filters.offset).limit(filters.limit)

            movies = []
            async for movie in cursor:
                movies.append(MovieInDB(**self._prepare_movie(movie)))

            return movies

        except Exception as e:
            logger.error(f"Error getting movies with filters: {e}")
            raise DatabaseException(f"Failed to get movies: {str(e)}")

    async def count(self, filters: MovieFilters) -> int:
        """Count movies with filters."""
        try:
            query = {}

            if filters.title:
                query["name"] = {"$regex": filters.title, "$options": "i"}

            if filters.genres:
                query["genres"] = {"$in": filters.genres}

            if filters.year_min or filters.year_max:
                year_query = {}
                if filters.year_min:
                    year_query["$gte"] = filters.year_min
                if filters.year_max:
                    year_query["$lte"] = filters.year_max
                query["year"] = year_query

            count = await self.collection.count_documents(query)
            return count

        except Exception as e:
            logger.error(f"Error counting movies: {e}")
            raise DatabaseException(f"Failed to count movies: {str(e)}")

    async def update(self, movie_id: str, movie_update: MovieUpdate) -> Optional[MovieInDB]:
        """Update a movie."""
        try:
            if not ObjectId.is_valid(movie_id):
                return None

            update_data = movie_update.model_dump(exclude_unset=True)

            if not update_data:
                return await self.get_by_id(movie_id)

            update_data["updated_at"] = datetime.utcnow()

            # Update slug if name is being updated
            if "name" in update_data:
                update_data["slug"] = slugify(update_data["name"])

            updated_movie = await self.collection.find_one_and_update(
                {"_id": ObjectId(movie_id)}, {"$set": update_data}, return_document=ReturnDocument.AFTER
            )

            if not updated_movie:
                return None

            return MovieInDB(**self._prepare_movie(updated_movie))

        except Exception as e:
            logger.error(f"Error updating movie {movie_id}: {e}")
            raise DatabaseException(f"Failed to update movie: {str(e)}")

    async def delete(self, movie_id: str) -> bool:
        """Delete a movie."""
        try:
            if not ObjectId.is_valid(movie_id):
                return False

            result = await self.collection.delete_one({"_id": ObjectId(movie_id)})
            return result.deleted_count > 0

        except Exception as e:
            logger.error(f"Error deleting movie {movie_id}: {e}")
            raise DatabaseException(f"Failed to delete movie: {str(e)}")

    def _prepare_movie(self, movie_doc: dict) -> dict:
        """Prepare movie document for Pydantic model."""
        if movie_doc and "_id" in movie_doc:
            movie_doc["_id"] = str(movie_doc["_id"])

        # Ensure required fields have defaults
        if "classification" not in movie_doc:
            movie_doc["classification"] = []

        if "created_at" not in movie_doc and "_id" in movie_doc:
            # Use ObjectId generation time as fallback
            movie_doc["created_at"] = ObjectId(movie_doc["_id"]).generation_time

        return movie_doc
