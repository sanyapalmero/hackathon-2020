#!/bin/sh -ex

python manage.py collectstatic --no-input

/app/docker/wait-for-it.sh ${POSTGRES_HOST:-db}:${POSTGRES_PORT:-5432}

python manage.py migrate

exec "$@"
