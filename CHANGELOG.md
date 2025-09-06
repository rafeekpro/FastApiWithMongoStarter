# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Comprehensive test suite with >80% coverage
- GitHub Actions CI/CD pipelines
- Security scanning with Bandit and Safety
- Contributing guidelines
- MIT License
- Changelog documentation

## [0.2.0] - 2024-01-06

### Added
- Clean architecture with repository pattern and service layer
- Comprehensive error handling with custom exceptions
- Docker support with multi-stage builds
- Docker Compose configuration for development
- Health check and readiness endpoints
- Pre-commit hooks configuration
- Black code formatter integration
- Comprehensive test infrastructure with pytest
- Type hints throughout the codebase
- MongoDB connection pooling with lifespan events
- Pydantic Settings for configuration management
- API documentation with Swagger/ReDoc
- Development configuration files (.env.example, .gitignore)
- Structured logging

### Changed
- Migrated to Pydantic V2
- Updated all dependencies to latest versions (FastAPI 0.115.5, Motor 3.6.0)
- Refactored project structure for better separation of concerns
- Improved MongoDB connection management
- Enhanced data validation with Pydantic validators
- Updated CORS configuration for better security

### Fixed
- Critical bugs in parameter mapping
- Typos in model fields (genres vs geners)
- Database connection string exposure in logs
- Undefined variables in configuration
- Import errors and unused imports

### Security
- Removed hardcoded secrets
- Added SECRET_KEY validation
- Implemented proper environment variable handling
- Configured CORS with specific allowed hosts

## [0.1.0] - 2024-01-01

### Added
- Initial FastAPI application setup
- Basic MongoDB integration with Motor
- Movie CRUD operations
- Basic project structure

[Unreleased]: https://github.com/yourusername/fastapi-mongodb-starter/compare/v0.2.0...HEAD
[0.2.0]: https://github.com/yourusername/fastapi-mongodb-starter/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/yourusername/fastapi-mongodb-starter/releases/tag/v0.1.0