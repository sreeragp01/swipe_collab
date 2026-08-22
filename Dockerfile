# ==============================================================================
# SwipeCollab Production Dockerfile for AWS EC2 / App Runner Deployment
# ==============================================================================
FROM python:3.11-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    curl \
    pkg-config \
    default-libmysqlclient-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy dependencies first for Docker caching
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . /app/

# Expose container port for ASGI server
EXPOSE 8000

# Run collectstatic & start Daphne ASGI server
CMD ["sh", "-c", "python manage.py collectstatic --no-input && daphne -b 0.0.0.0 -p 8000 config.asgi:application"]
