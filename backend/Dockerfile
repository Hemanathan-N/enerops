# Use an official lightweight Python runtime
FROM python:3.11-slim

# Prevent Python from writing .pyc files to disc and enable unbuffered output logging
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Set workspace directory
WORKDIR /app

# Install system dependencies required for building PostgreSQL drivers (libpq)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy dependency requirements file first (enables Docker build caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy backend application source code
COPY . .

# Expose port FastAPI runs on
EXPOSE 8000
RUN chmod +x /app/entrypoint.sh

# Run FastAPI app using Uvicorn
ENTRYPOINT ["/app/entrypoint.sh"]
