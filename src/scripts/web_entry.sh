#!/bin/sh

python ./manage.py collectstatic --noinput
python ./manage.py migrate
python ./manage.py runserver 0:8000