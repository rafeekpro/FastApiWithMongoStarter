# Contributing to FastAPI MongoDB Starter

First off, thank you for considering contributing to FastAPI MongoDB Starter! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check existing issues as you might find out that you don't need to create one. When you are creating a bug report, please include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include screenshots if relevant**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and explain which behavior you expected to see instead**
* **Explain why this enhancement would be useful**

### Pull Requests

1. Fork the repo and create your branch from `master`
2. If you've added code that should be tested, add tests
3. If you've changed APIs, update the documentation
4. Ensure the test suite passes
5. Make sure your code follows the existing code style
6. Issue that pull request!

## Development Process

### Setting Up Development Environment

1. Fork and clone the repository:
   ```bash
   git clone https://github.com/yourusername/fastapi-mongodb-starter.git
   cd fastapi-mongodb-starter
   ```

2. Create a virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   pip install -e ".[dev]"
   ```

4. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

5. Set up environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

6. Run MongoDB using Docker:
   ```bash
   docker-compose up -d mongodb
   ```

### Code Style

We use the following tools to maintain code quality:

* **Black** for code formatting (line length: 120)
* **Ruff** for linting
* **mypy** for type checking

Before committing, run:
```bash
black app tests
ruff check app tests --fix
mypy app
```

Or let pre-commit handle it automatically.

### Testing

Write tests for any new functionality. We aim for >80% test coverage.

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=app --cov-report=html

# Run specific test file
pytest tests/unit/test_schemas.py

# Run only unit tests
pytest tests/unit/

# Run only integration tests
pytest tests/integration/
```

### Commit Messages

We follow conventional commits specification:

* `feat:` New feature
* `fix:` Bug fix
* `docs:` Documentation changes
* `style:` Code style changes (formatting, missing semicolons, etc.)
* `refactor:` Code refactoring
* `test:` Adding or updating tests
* `chore:` Maintenance tasks
* `perf:` Performance improvements

Examples:
```
feat: add user authentication endpoint
fix: resolve database connection timeout issue
docs: update API documentation for movies endpoint
test: add unit tests for movie service
```

### Documentation

* Keep README.md up to date
* Document all API endpoints
* Add docstrings to all functions and classes
* Update CHANGELOG.md for significant changes

### Branch Naming

* `feature/` for new features (e.g., `feature/user-auth`)
* `fix/` for bug fixes (e.g., `fix/db-connection`)
* `docs/` for documentation (e.g., `docs/api-update`)
* `refactor/` for refactoring (e.g., `refactor/service-layer`)

## Review Process

1. All submissions require review
2. Continuous Integration must pass
3. Code coverage should not decrease
4. Follow the existing code style
5. Update documentation as needed

## Release Process

1. Update version in `pyproject.toml`
2. Update CHANGELOG.md
3. Create a pull request
4. After merge, create a release tag
5. GitHub Actions will handle deployment

## Questions?

Feel free to open an issue with your question or reach out to the maintainers.

Thank you for contributing! 🎉