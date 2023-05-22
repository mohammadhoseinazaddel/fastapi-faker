# Wallpay Services

Wallpay Fast API Application For Backend Services

## Local Deployment

```bash
docker compose up -d
```

## Dependency Installation and Management

If you want to create the virtualenv inside the project’s root directory specify:

```bash
poetry config virtualenvs.in-project true
```

If you do not specify the virtualenv is going to be kept inside poetry directory.

### Source the virtual environment

```bash
poetry shell
```

### Add new dependencies

```bash
poetry add [package-name]
```

### Remove dependencies

```bash
poetry remove [package-name]
```

### Install all dependencies

```bash
poetry install
```

### Install dependecies excluding developments

```bash
poetry install --without dev
```

### Execute one of the scripts defined in pyproject.toml.

```bash
poetry run my-script
```

### Exports the lock file to requirements.txt

```bash
poetry export -f requirements.txt —output requirements.txt
```

### Exit poetry

```bash
exit
```

### Deactivate poetry

```bash
deactivate
```

## Task Queue

In order to add module tasks to a worker, the module name should be defined in the celery queue list with the CELERY_QUEUES environment variable of that worker. Also, the module must be defined in system/celery/setup.py inside a list as the argument of TaskRouter initiation. e.g.:

```python
from .router import TaskRouter

modules: List[str] = ['my_module']
router = TaskRouter(modules)
```

Tasks themseleves must be defined inside the "task" directory of the module root directory. Any .py file will get imported recursively as task and any .yml or .yaml file will get imported recursively as schedule file.

### Example task

```python
from system.celery import app

@app.task
def my_task():
    pass
```

### Example schedule

```yaml
task-name:
  task: "my_module.tasks.my_task"
  schedule: 600 # Seconds
```

Schedule definition supports the crontab function and any key inside the "schedule" will get unpacked to the celery crontab function. e.g.:

```yaml
task-name:
  task: "my_module.tasks.my_task"
  schedule:
    hour: 8
    minute: 30
```

### Example seeder

if you want change the number of each model fake data ind it in initial_fake_data.py find your model there and change the number to number that you want

```bash
bash scripts/generate-fake-data.sh
```

