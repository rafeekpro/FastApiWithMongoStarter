import logging
from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase

from app.core.settings import settings

logger = logging.getLogger(__name__)


class Database:
    client: Optional[AsyncIOMotorClient] = None
    database: Optional[AsyncIOMotorDatabase] = None


db = Database()


async def connect_to_mongo() -> None:
    """Create database connection."""
    try:
        logger.info("Connecting to MongoDB...")
        db.client = AsyncIOMotorClient(
            settings.MONGODB_URL,
            maxPoolSize=settings.MAX_CONNECTIONS_COUNT,
            minPoolSize=settings.MIN_CONNECTIONS_COUNT,
        )
        
        # Verify connection
        await db.client.admin.command("ping")
        
        db.database = db.client[settings.MONGO_DB]
        logger.info("Successfully connected to MongoDB!")
        
    except Exception as e:
        logger.error(f"Failed to connect to MongoDB: {e}")
        raise


async def close_mongo_connection() -> None:
    """Close database connection."""
    try:
        if db.client:
            logger.info("Closing MongoDB connection...")
            db.client.close()
            logger.info("MongoDB connection closed!")
    except Exception as e:
        logger.error(f"Error closing MongoDB connection: {e}")


def get_database() -> AsyncIOMotorDatabase:
    """Get database instance."""
    if not db.database:
        raise RuntimeError("Database is not initialized")
    return db.database


def get_collection(collection_name: str):
    """Get collection from database."""
    if not db.database:
        raise RuntimeError("Database is not initialized")
    return db.database[collection_name]