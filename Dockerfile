FROM python:3.12-slim

# Install system-level geospatial libraries GeoDjango needs
RUN apt-get update && apt-get install -y \
    binutils \
    libproj-dev \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install Python dependencies first (better Docker layer caching)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the project
COPY . .

# Collect static files at build time
RUN python manage.py collectstatic --no-input

# Run migrations, then start gunicorn
# Copy the project
COPY . .

# Collect static files
RUN python manage.py collectstatic --no-input

# Start the Django application
CMD ["sh", "-c", "gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-10000}"]