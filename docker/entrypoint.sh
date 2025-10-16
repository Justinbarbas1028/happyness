#!/usr/bin/env sh
set -e

# Wait for Postgres if configured
if [ -n "$POSTGRES_HOST" ]; then
  echo "Waiting for Postgres at $POSTGRES_HOST:$POSTGRES_PORT..."
  until python - <<PY
import sys
import time
import os
import psycopg

host=os.environ.get('POSTGRES_HOST','localhost')
port=int(os.environ.get('POSTGRES_PORT','5432'))
user=os.environ.get('POSTGRES_USER','postgres')
password=os.environ.get('POSTGRES_PASSWORD','postgres')
db=os.environ.get('POSTGRES_DB','postgres')

for i in range(60):
    try:
        with psycopg.connect(host=host, port=port, user=user, password=password, dbname=db, connect_timeout=2):
            print('Postgres is up!')
            sys.exit(0)
    except Exception as e:
        print('Postgres not ready yet:', e)
        time.sleep(1)
print('Timed out waiting for Postgres')
sys.exit(1)
PY
  do
    sleep 1
  done
fi

# Django setup
python manage.py migrate --noinput

# Optional: collect static (safe even if not configured)
python manage.py collectstatic --noinput || true

# Start server (gunicorn)
exec gunicorn happyness.wsgi:application --bind 0.0.0.0:8000 --workers ${GUNICORN_WORKERS:-3}
