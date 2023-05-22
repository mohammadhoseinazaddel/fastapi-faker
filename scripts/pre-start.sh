#!/bin/bash

# Change Workdir
# shellcheck disable=SC2164
cd app

# Let the DB start
python backend_pre_start.py

# Run migrations
#alembic revision --autogenerate -m "created_by_pre_start_command"
alembic upgrade head


# Create initial data in DB
python initial_data.py
