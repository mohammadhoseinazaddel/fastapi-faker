#!/bin/bash
set -e

cd app

if [ $APP_ENV = production ]; then
    celery -A system.celery flower;
else
    celery -A system.celery flower;
fi
