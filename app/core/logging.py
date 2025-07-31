# app/core/logging_config.py

import logging
import logging.config
import os
import sys

import structlog

from app.core.config import settings

LOG_FILE_PATH = settings.LOG_FILE
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5

def setup_logging() -> None:
    """
    Set up unified logging configuration using structlog.

    Logs will only be written to LOG_FILE_PATH if settings.SAVE_LOG is True.
    """
    log_level = "DEBUG" if settings.DEBUG else "INFO"

    # Define shared processors for structlog
    shared_processors = [
        structlog.stdlib.add_log_level,
        structlog.stdlib.add_logger_name,
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.stdlib.PositionalArgumentsFormatter(),
    ]

    # Configure structlog itself
    structlog.configure(
        processors=shared_processors + [
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ],
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # Determine the renderer based on whether structured logging is enabled
    renderer = (
        structlog.processors.JSONRenderer()
        if settings.STRUCTURED_LOGGING
        else structlog.dev.ConsoleRenderer(colors=True)
    )

    # Define the base logging configuration
    logging_config = {
        "version": 1,
        "disable_existing_loggers": False,
        "formatters": {
            "default": {
                "()": "structlog.stdlib.ProcessorFormatter",
                "processor": renderer,
                "foreign_pre_chain": shared_processors,
            },
        },
        "handlers": {
            "console": {
                "class": "logging.StreamHandler",
                "formatter": "default",
                "stream": sys.stdout,
            },
        },
        "loggers": {
            # Root logger configuration
            "": {"level": log_level, "propagate": True},
            # Uvicorn loggers configuration
            "uvicorn.access": {"level": log_level, "propagate": False},
            "uvicorn.error": {"level": "ERROR", "propagate": False},
            "uvicorn": {"level": log_level, "propagate": False},
        },
    }

    # Define which handlers are active
    active_handlers = ["console"]

    # Conditionally add the file handler if SAVE_LOG is enabled
    if settings.SAVE_LOG:
        os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)
        logging_config["handlers"]["file"] = {
            "class": "logging.handlers.RotatingFileHandler",
            "formatter": "default",
            "filename": LOG_FILE_PATH,
            "maxBytes": MAX_LOG_SIZE,
            "backupCount": BACKUP_COUNT,
        }
        active_handlers.append("file")

    # Apply the active handlers to all configured loggers
    for logger_name in logging_config["loggers"]:
        logging_config["loggers"][logger_name]["handlers"] = active_handlers

    # Apply the final configuration
    logging.config.dictConfig(logging_config)


def get_logger(name: str) -> structlog.stdlib.BoundLogger:
    """
    Get a structlog logger.
    """
    return structlog.get_logger(name)
