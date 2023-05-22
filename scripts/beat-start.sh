#!/bin/bash
set -e

cd app

if [ $APP_ENV = production ]; then
    celery -A system.celery.beat beat --loglevel=INFO;
else
    celery -A system.celery.beat beat --loglevel=DEBUG;
fi
