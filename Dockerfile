FROM python:3.12-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Create app user
RUN groupadd app \
 && useradd -r -g app app

WORKDIR /app

# System dependencies (ROOT)
RUN apt-get update \
 && apt-get install -y --no-install-recommends \
    gcc libpq-dev curl \
 && rm -rf /var/lib/apt/lists/*

# Python dependencies (ROOT)
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir -r requirements.txt \
 && pip install --no-cache-dir gunicorn

# Project files
COPY . .

# Build-time Django env (SAFE DUMMY)
ENV SECRET_KEY=super-secret
ENV DB_ENGINE=django.db.backends.sqlite3
ENV DB_NAME=/tmp/db.sqlite3
ENV DB_USERNAME=dummy
ENV DB_PASSWORD=dummy
ENV DB_HOST=localhost
ENV DB_PORT=5432
ENV DEBUG=False
ENV LANGUAGE_CODE=en-us
ENV TIME_ZONE=UTC
ENV REDIS=redis://127.0.0.1:6379/1

# Static files
RUN mkdir -p /app/staticfiles \
 && python manage.py collectstatic --noinput

# Permissions
RUN chown -R app:app /app

# Drop privileges
USER app

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "core.wsgi:application"]
