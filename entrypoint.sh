set -e

cd /app/

python manage.py migrate

exec "$@"
