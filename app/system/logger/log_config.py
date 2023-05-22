LOG_CONFIG = {
    "version": 1,
    "formatters": {
        "simple": {
            "format": "%(asctime)s %(name)-12s %(levelname)-8s %(message)s"
        },
        "verbose": {
            "format": "%(levelname)3.3s %(asctime)22.22s %(process)7d [%(name)s:%(funcName)s] %(message)s"
        }
    },
    "handlers": {
        "null": {
            "level": "DEBUG",
            "class": "logging.NullHandler"
        },
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler"
        }
    },
    "root": {
        "handlers": [
            "console"
        ],
        "level": "INFO"
    },
    "loggers": {
        "": {
            "handlers": [
                "console"
            ],
            "level": "INFO",
        },
        "urllib3": {
            "level": "WARN"
        },
        "amqp": {
            "handlers": [
                "console"
            ],
            "level": "WARN"
        }
    }
}

