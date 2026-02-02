#!/bin/bash

# Vectra Setup Script

echo "🚀 Setting up Vectra development environment..."

# Check prerequisites
echo "Checking prerequisites..."
command -v python3 >/dev/null 2>&1 || { echo "❌ Python 3 is required"; exit 1; }
command -v node >/dev/null 2>&1 || { echo "❌ Node.js is required"; exit 1; }
command -v docker >/dev/null 2>&1 || { echo "❌ Docker is required"; exit 1; }

# Backend setup
echo "📦 Setting up backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
pip install -r requirements-dev.txt
cd ..

# Frontend setup
echo "📦 Setting up frontend..."
cd frontend
npm install
cd ..

# Docker setup
echo "🐳 Starting Docker services..."
docker-compose up -d postgres redis

echo "✅ Setup complete!"
echo ""
echo "Next steps:"
echo "1. Copy .env.example to .env in both backend and frontend"
echo "2. Update .env files with your configuration"
echo "3. Run 'make migrate' to setup the database"
echo "4. Run 'make dev' to start development servers"
