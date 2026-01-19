#!/bin/bash

# Vectra Development Script

echo "🚀 Starting Vectra development environment..."

# Start Docker services
echo "🐳 Starting Docker services..."
docker-compose up -d postgres redis

# Wait for services to be ready
echo "⏳ Waiting for services to be ready..."
sleep 5

# Start backend
echo "🔧 Starting backend..."
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000 &
BACKEND_PID=$!
cd ..

# Start Celery worker
echo "⚙️  Starting Celery worker..."
cd backend
celery -A app.tasks.celery_app worker --loglevel=INFO &
CELERY_PID=$!
cd ..

# Start frontend
echo "🎨 Starting frontend..."
cd frontend
npm run dev &
FRONTEND_PID=$!
cd ..

echo "✅ All services started!"
echo ""
echo "Backend: http://localhost:8000"
echo "Frontend: http://localhost:3000"
echo "API Docs: http://localhost:8000/docs"
echo ""
echo "Press Ctrl+C to stop all services"

# Wait for interrupt
trap "kill $BACKEND_PID $CELERY_PID $FRONTEND_PID; docker-compose down; exit" INT
wait
