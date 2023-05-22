#!/bin/bash

# Change Workdir
# shellcheck disable=SC2164
cd app

# Let the main app start
if [ $APP_ENV = production ]; then
    newrelic-admin run-program uvicorn main:app --host 0.0.0.0 --port 8000;
else
    newrelic-admin run-program uvicorn main:app --host 0.0.0.0 --port 8000 --reload;
fi
