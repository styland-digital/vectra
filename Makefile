.PHONY: help install dev test lint build deploy migrate migrate-new seed clean docker-up docker-down

help:
	@echo "Vectra - Available commands:"
	@echo "  make install       - Install all dependencies"
	@echo "  make dev           - Start development environment"
	@echo "  make docker-up     - Start Docker services (postgres, redis)"
	@echo "  make docker-down   - Stop Docker services"
	@echo "  make test          - Run all tests"
	@echo "  make lint          - Run linters"
	@echo "  make build         - Build for production"
	@echo "  make migrate       - Run database migrations"
	@echo "  make migrate-new   - Create new migration (use: make migrate-new msg='description')"
	@echo "  make seed          - Seed database with test data"
	@echo "  make clean         - Clean temporary files and caches"

install:
	@echo "Installing backend dependencies..."
	cd backend && python -m venv venv || true
	cd backend && pip install -r requirements.txt
	cd backend && pip install -r requirements-dev.txt
	@echo "Installing frontend dependencies..."
	cd frontend && npm install
	@echo "✅ Installation complete!"

dev:
	@echo "Starting development environment..."
	@echo "Make sure Docker services are running: make docker-up"
	@echo "Backend: http://localhost:8000"
	@echo "Frontend: http://localhost:3000"
	@echo "API Docs: http://localhost:8000/docs"

docker-up:
	@echo "Starting Docker services..."
	docker-compose up -d postgres redis
	@echo "Waiting for services to be ready..."
	@sleep 5
	@echo "✅ Docker services started!"

docker-down:
	@echo "Stopping Docker services..."
	docker-compose down
	@echo "✅ Docker services stopped!"

test:
	@echo "Running backend tests..."
	cd backend && pytest --cov=app --cov-report=term-missing
	@echo "Running frontend tests..."
	cd frontend && npm run test

test-e2e:
	@echo "Running E2E tests..."
	cd frontend && npm run test:e2e

lint:
	@echo "Linting backend..."
	cd backend && black . --check || black .
	cd backend && ruff check . || ruff check . --fix
	@echo "Linting frontend..."
	cd frontend && npm run lint

build:
	@echo "Building backend..."
	cd backend && docker build -t vectra-backend .
	@echo "Building frontend..."
	cd frontend && npm run build

migrate:
	@echo "Running database migrations..."
	cd backend && alembic upgrade head

migrate-new:
	@if [ -z "$(msg)" ]; then \
		echo "❌ Error: Please provide a message. Usage: make migrate-new msg='description'"; \
		exit 1; \
	fi
	cd backend && alembic revision --autogenerate -m "$(msg)"

seed:
	@echo "Seeding database..."
	cd backend && python -m scripts.seed_database

clean:
	@echo "Cleaning temporary files..."
	docker-compose down -v || true
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .next -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name node_modules -exec rm -rf {} + 2>/dev/null || true
	@echo "✅ Clean complete!"
