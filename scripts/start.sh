#!/bin/bash

echo "🚀 Starting Project Management API..."

# Check if Docker is running
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker is not running. Please start Docker."
    exit 1
fi

echo "📦 Building and starting containers..."
docker-compose up --build -d

echo "⏳ Waiting for database to be ready..."
sleep 10

echo "🔄 Applying migrations..."
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

echo "✅ Project started successfully!"
echo "🌐 API available at: http://localhost:8000"
echo "📚 Swagger documentation: http://localhost:8000/api/docs/"
echo "🔧 Django Admin: http://localhost:8000/admin/"

echo "📊 Checking database connection..."
docker-compose exec web python manage.py check_db