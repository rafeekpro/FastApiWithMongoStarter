# FastAPI MongoDB Starter 🚀

Modern, production-ready FastAPI application with MongoDB integration, featuring clean architecture, comprehensive testing, and Docker support.

## Features ✨

- **FastAPI** - Modern, fast web framework for building APIs
- **MongoDB** - NoSQL database with Motor async driver
- **Pydantic V2** - Data validation using Python type annotations
- **Clean Architecture** - Repository pattern, service layer, dependency injection
- **Docker Support** - Development and production Docker configurations
- **Testing** - Comprehensive test suite with pytest
- **Type Safety** - Full type hints with mypy validation
- **Pre-commit Hooks** - Code quality enforcement
- **Health Checks** - Ready and liveness probes
- **CRUD Operations** - Complete Create, Read, Update, Delete functionality

## Project Structure 📁

```
app/
├── api/              # API endpoints and dependencies
│   ├── api_v1/       # API version 1
│   │   ├── endpoints/    # Route handlers
│   │   └── api.py        # API router
│   └── deps.py       # Dependency injection
├── core/             # Core functionality
│   ├── settings.py   # Application settings
│   └── exceptions.py # Custom exceptions
├── db/               # Database configuration
│   └── database.py   # MongoDB connection
├── models/           # Database models
├── schemas/          # Pydantic schemas
├── services/         # Business logic
├── repositories/     # Data access layer
└── main.py          # Application entry point
```

## Requirements 📋

- Python 3.11+
- MongoDB 7.0+ (or Docker)
- pip or poetry

## Quick Start 🏃

### 1. Clone the repository

```bash
git clone https://github.com/yourusername/fastapi-mongodb-starter.git
cd fastapi-mongodb-starter
```

### 2. Set up environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Configure environment variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env with your configuration
# Generate a secure SECRET_KEY:
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

### 4. Run with Docker (Recommended)

```bash
# Start all services (app, MongoDB, Mongo Express)
docker-compose up -d

# View logs
docker-compose logs -f app

# Stop services
docker-compose down
```

The application will be available at:
- API: http://localhost:8000
- API Documentation: http://localhost:8000/docs
- Mongo Express: http://localhost:8081 (admin/admin)

### 5. Run locally (without Docker)

```bash
# Make sure MongoDB is running locally
# Update .env with your MongoDB connection details

# Run the application
uvicorn app.main:app --reload

# Or with custom host/port
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

## API Documentation 📚

Once the application is running, you can access:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI Schema**: http://localhost:8000/openapi.json

### Available Endpoints

#### Movies
- `GET /api/v1/movies` - List all movies with pagination
- `GET /api/v1/movies/{movie_id}` - Get movie by ID
- `GET /api/v1/movies/slug/{slug}` - Get movie by slug
- `POST /api/v1/movies` - Create a new movie
- `PUT /api/v1/movies/{movie_id}` - Update a movie
- `DELETE /api/v1/movies/{movie_id}` - Delete a movie

#### Health
- `GET /health` - Health check
- `GET /ready` - Readiness probe

## Development 🛠️

### Install development dependencies

```bash
pip install -r requirements.txt
# or
pip install -e ".[dev]"
```

### Run tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_schemas.py

# Run with verbose output
pytest -v
```

### Code quality

```bash
# Format code
ruff format .

# Lint code
ruff check . --fix

# Type checking
mypy app

# Install pre-commit hooks
pre-commit install

# Run pre-commit on all files
pre-commit run --all-files
```

## Production Deployment 🚢

### Using Docker

```bash
# Build production image
docker build -t fastapi-app .

# Run production container
docker run -d \
  -p 8000:8000 \
  -e MONGODB_URL="mongodb://user:pass@host:27017/db" \
  -e SECRET_KEY="your-production-secret-key" \
  --name fastapi-app \
  fastapi-app
```

### Environment Variables

Required for production:
- `SECRET_KEY` - Secret key for security (generate a strong one!)
- `MONGODB_URL` - MongoDB connection string
- `ALLOWED_HOSTS` - Comma-separated list of allowed hosts

Optional:
- `DEBUG` - Set to false in production (default: false)
- `PROJECT_NAME` - Application name
- `MAX_CONNECTIONS_COUNT` - MongoDB max connections
- `MIN_CONNECTIONS_COUNT` - MongoDB min connections

## Database Schema 📊

### Movie Collection

```javascript
{
  "_id": ObjectId,
  "name": String,
  "casts": [String],
  "genres": [String],
  "year": Number,
  "slug": String,
  "classification": [
    {
      "country": String,
      "value": String
    }
  ],
  "created_at": DateTime,
  "updated_at": DateTime
}
```

### Indexes
- `slug` - Unique index
- `name` - Text index for search
- `year` - Regular index
- `genres` - Regular index

## Contributing 🤝

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License 📄

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgments 🙏

- Inspired by [fastapi-mongodb-realworld-example-app](https://github.com/markqiu/fastapi-mongodb-realworld-example-app)
- Built with [FastAPI](https://fastapi.tiangolo.com/)
- Database powered by [MongoDB](https://www.mongodb.com/)