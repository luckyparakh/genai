import logging

# Custom logging setup

# The root logger in Python's logging system is the default logger provided by the logging module. 
# If no custom logger is defined or used, the root logger is invoked by 
# default when logging functions like logging.info() or logging.error() are called without specifying a logger.

LOGGING_CONFIG = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        "default": {
            "format": "%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s",
        },
    },
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
            "formatter": "default",
        },
    },
    "root": {
        "level": "INFO",
        "handlers": ["console"],
    },
    "loggers": {
        "api_logger": {
            "level": "DEBUG",
            "handlers": ["console"],
            "propagate": False,
        },
    },
}