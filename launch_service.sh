#!/bin/bash

celery -A celery_app worker -l info &

gunicorn -c /usr/src/flaskProxy/gunicorn.py manager:app
