#!/bin/bash

echo "🚀 Запуск проекта Project Management API..."

# Проверяем, что Docker запущен
if ! docker info > /dev/null 2>&1; then
    echo "❌ Docker не запущен. Пожалуйста, запустите Docker."
    exit 1
fi

echo "📦 Сборка и запуск контейнеров..."
docker-compose up --build -d

echo "⏳ Ожидание готовности базы данных..."
sleep 10

echo "🔄 Применение миграций..."
docker-compose exec web python manage.py makemigrations
docker-compose exec web python manage.py migrate

echo "✅ Проект запущен!"
echo "🌐 API доступно по адресу: http://localhost:8000"
echo "📚 Swagger документация: http://localhost:8000/api/docs/"
echo "🔧 Django Admin: http://localhost:8000/admin/"

echo "📊 Проверка подключения к базе данных..."
docker-compose exec web python manage.py check_db