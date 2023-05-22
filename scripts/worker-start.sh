#!/bin/bash
set -e

cd app

if [ $APP_ENV = production ]; then
    celery \
        -A system.celery worker \
        --loglevel=INFO \
        -Q $([[ ! -z "$CELERY_QUEUES" ]] && echo "$CELERY_QUEUES" || echo "wallpay-tasks") \
        -c 1 \
        -n $([[ ! -z "$CELERY_WORKER_NAME" ]] && echo "$CELERY_WORKER_NAME" || echo "wallpay_worker")@%h;
else
    celery \
        -A system.celery worker \
        --loglevel=DEBUG \
        -Q $([[ ! -z "$CELERY_QUEUES" ]] && echo "$CELERY_QUEUES" || echo "wallpay-tasks") \
        -c 1 \
        -n $([[ ! -z "$CELERY_WORKER_NAME" ]] && echo "$CELERY_WORKER_NAME" || echo "wallpay_worker")@%h;
fi
