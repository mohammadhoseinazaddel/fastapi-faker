FROM python:3.11.3-slim-bullseye

LABEL name="Wallpay Services"
LABEL maintainer="Pourya Moghadam <p.moghadam@wallex.net>"
LABEL version="0.0.21"

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Production/development
ARG YOUR_ENV=development

EXPOSE 8000
EXPOSE 5555

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

ENV YOUR_ENV=${YOUR_ENV} \
    PYTHONFAULTHANDLER=1 \
    PYTHONHASHSEED=random \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    POETRY_VERSION=1.4.2 \
    LC_ALL=C.UTF-8 \
    LANG=C.UTF-8

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        libpq-dev \
        gcc

ENV PROJECT_DIR=wallpay
WORKDIR /$PROJECT_DIR
COPY . .

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false && \
    poetry install $(test "$YOUR_ENV" == production && echo "--without dev")

# Creates a non-root user with an explicit UID and adds permission to access the $PROJECT_DIR folder
ENV USERNAME=wallpay
RUN adduser -u 1000 --disabled-password --gecos "" $USERNAME && \
    chown -R $USERNAME /$PROJECT_DIR
USER $USERNAME

RUN chmod a+x scripts/*.sh
ENTRYPOINT [ "./scripts/docker-entrypoint.sh" ]
