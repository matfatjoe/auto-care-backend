#!/bin/sh
set -e

POSTGRES_HOST=${POSTGRES_HOST:-psql}
POSTGRES_PORT=${POSTGRES_PORT:-5432}

echo "🔍 Esperando o PostgreSQL em $POSTGRES_HOST:$POSTGRES_PORT..."

while ! nc -z $POSTGRES_HOST $POSTGRES_PORT; do
  echo "🟡 Aguardando PostgreSQL subir..."
  sleep 2
done

echo "✅ PostgreSQL disponível em $POSTGRES_HOST:$POSTGRES_PORT"

python manage.py collectstatic --noinput
python manage.py makemigrations --noinput
python manage.py migrate --noinput
python manage.py runserver 0.0.0.0:8000
