.PHONY: bootstrap api lint test clean

# Install dependencies
bootstrap:
	@echo "Installing dependencies..."
	uv sync

# Run API server
api:
	@echo "Starting API server..."
	uv run uvicorn apps.api.main:app --reload --host 0.0.0.0 --port 8000

# Run linting and formatting
lint:
	@echo "Running formatters and linters..."
	uv run black .
	uv run ruff check . --fix

# Run tests
test:
	@echo "Running tests..."
	uv run pytest tests/ -v

# Run tests with coverage
test-cov:
	@echo "Running tests with coverage..."
	uv run pytest tests/ -v --cov=apps --cov=packages --cov-report=term-missing --cov-report=html

# Generate sample data
sample-data:
	@echo "Generating sample data..."
	uv run python data/sample/generate_sample_data.py

# Clean up
clean:
	@echo "Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .coverage htmlcov
	rm -f antleads.db

# Help
help:
	@echo "Available commands:"
	@echo "  make bootstrap    - Install all dependencies"
	@echo "  make api          - Run API server in development mode"
	@echo "  make lint         - Run formatters and linters"
	@echo "  make test         - Run test suite"
	@echo "  make test-cov     - Run tests with coverage report"
	@echo "  make sample-data  - Generate sample data"
	@echo "  make clean        - Clean up generated files"
