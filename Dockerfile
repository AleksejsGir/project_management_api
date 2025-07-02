# --- Stage 1: Builder ---
FROM python:3.11-slim as builder

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Install "heavy" dependencies that won't go into the final image
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Create isolated virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Copy and install dependencies into venv
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code
COPY . .

# Collect static files into /app/staticfiles folder
RUN python manage.py collectstatic --noinput --clear


# --- Stage 2: Final Image ---

FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Copy only the ready venv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

# Create user without root privileges
RUN addgroup --system app && adduser --system --group app

WORKDIR /app

# Copy ONLY code and collected static files from builder
COPY --from=builder /app/staticfiles ./staticfiles
COPY . .

# Change file ownership to our secure user
RUN chown -R app:app /app

# Switch to unprivileged user
USER app

# Expose port 8000 for Railway
EXPOSE 8000

# CMD command is NOT used since Railway uses startCommand
CMD ["python", "-m", "gunicorn", "project_management.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2"]