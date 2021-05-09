#!/bin/bash

celery -A celery_app worker -l info &

gunicorn -c /usr/src/flaskServer/gunicorn.py manager:app
