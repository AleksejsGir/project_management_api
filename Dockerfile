# --- Этап 1: Сборщик (Builder) ---
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Ставим "тяжелые" зависимости, которые не попадут в финальный образ
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Создаем изолированное виртуальное окружение
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Копируем и устанавливаем зависимости в venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код
COPY . .

# Собираем статику в папку /app/staticfiles
RUN python manage.py collectstatic --noinput --clear


# --- Этап 2: Финальный образ (Final Image) ---

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Копируем только готовое venv из сборщика
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Создаем пользователя без прав root
RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# Копируем ТОЛЬКО код и собранную статику из сборщика
COPY --from=builder /app/staticfiles ./staticfiles
COPY . .

# Меняем владельца файлов на нашего безопасного пользователя
RUN chown -R app:app /app

# Переключаемся на непривилегированного пользователя
USER app

# Expose port 8000 (стандартный для Railway)
EXPOSE 8000

# CMD для Railway - использует фиксированный порт
CMD gunicorn project_management.wsgi:application --bind 0.0.0.0:8000 --workers 2 --timeout 120