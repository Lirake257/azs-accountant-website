FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    libxml2-dev libxslt1-dev zlib1g-dev libpq-dev gcc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .


CMD ["sh", "-c", "\
python manage.py migrate --noinput && \
python manage.py shell -c \"from django.contrib.auth import get_user_model; User=get_user_model(); User.objects.filter(username='admin').exists() or User.objects.create_superuser('admin','admin@example.com','Admin123456')\" && \
python manage.py collectstatic --noinput && \
gunicorn core.wsgi:application --bind 0.0.0.0:${PORT:-8080}"]