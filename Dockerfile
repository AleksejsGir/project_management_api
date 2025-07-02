FROM python:3.11-slim

# Установка системных зависимостей
RUN apt-get update && apt-get install -y \
    gcc \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Установка Python зависимостей (кэшируется, если requirements.txt не изменился)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копирование кода приложения
COPY . .

# Создание staticfiles директории
RUN mkdir -p staticfiles

# Контрольная команда
RUN echo "Build completed at $(date)"

# Создание пользователя для безопасности (в продакшене-Best practice для Docker контейнеров)
# RUN adduser --disabled-password --gecos '' appuser && chown -R appuser /app
# USER appuser

EXPOSE 8000

# Production команда (gunicorn через Procfile)
CMD ["gunicorn", "project_management.wsgi", "--bind", "0.0.0.0:8000"]