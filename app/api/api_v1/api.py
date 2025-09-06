from fastapi import APIRouter

from .endpoints.movies import router as movie_router

router = APIRouter()
router.include_router(movie_router)
