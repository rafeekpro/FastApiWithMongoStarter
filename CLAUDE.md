# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

### Development Server
```bash
uvicorn app.main:app --reload
```

### Install Dependencies
```bash
pip install -r requirements.txt
```

## Architecture

This is a FastAPI application with MongoDB integration following a layered architecture:

### Core Components

- **app/main.py**: FastAPI application entry point that configures CORS, event handlers for MongoDB connection lifecycle, and exception handlers
- **app/core/config.py**: Configuration management using environment variables with dotenv, defines MongoDB connection parameters and application settings
- **app/db/**: Database layer using Motor (async MongoDB driver)
  - Connection singleton pattern in `mongodb.py` 
  - Connection lifecycle management in `mongodb_utils.py`
  
### API Structure

Routes follow versioned API pattern:
- **app/api/api_v1/api.py**: Main API router that aggregates all endpoint routers
- **app/api/api_v1/endpoints/**: Individual endpoint modules (currently `movie.py`)
- All API routes are prefixed with `/api` (defined in `API_V1_STR`)

### Data Flow

1. **Models** (app/models/): Pydantic models for request/response validation
   - Base models extend `RWModel` for consistent JSON aliasing
   - Database models use mixins (`DBModelMixin`, `DateTimeModelMixin`) for common fields
   
2. **CRUD Operations** (app/crud/): Database operations layer
   - Direct MongoDB collection access via Motor's AsyncIOMotorClient
   - Returns domain models populated from database documents
   
3. **API Endpoints**: FastAPI route handlers that orchestrate CRUD operations and return validated responses

### MongoDB Configuration

- Connection string built from environment variables or `MONGODB_URL` directly
- Database name: Configured via `MONGO_DB` env var (defaults to "fastapi")
- Collections: Currently uses "movie" collection
- Connection pooling: Configurable via `MAX_CONNECTIONS_COUNT` and `MIN_CONNECTIONS_COUNT`

### Environment Variables

Required `.env` file with:
- `MONGODB_URL` or individual MongoDB connection parameters (`MONGO_HOST`, `MONGO_PORT`, `MONGO_USER`, `MONGO_PASSWORD`, `MONGO_DB`)
- `SECRET_KEY` for application security
- `PROJECT_NAME` for API documentation
- `ALLOWED_HOSTS` for CORS configuration