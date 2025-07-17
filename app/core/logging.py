import logging
import sys
import os
from logging.handlers import RotatingFileHandler
from pythonjsonlogger import jsonlogger
from colorama import Fore, Style, init as colorama_init

from app.core.config import settings

colorama_init(autoreset=True)

LOG_LEVEL_COLORS = {
    logging.DEBUG: Fore.CYAN,
    logging.INFO: Fore.GREEN,
    logging.WARNING: Fore.YELLOW,
    logging.ERROR: Fore.RED,
    logging.CRITICAL: Fore.MAGENTA + Style.BRIGHT,
}

LOG_FILE_PATH = "logs/app.log"
MAX_LOG_SIZE = 10 * 1024 * 1024  # 10 MB
BACKUP_COUNT = 5


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        color = LOG_LEVEL_COLORS.get(record.levelno, "")
        message = super().format(record)
        return f"{color}{message}{Style.RESET_ALL}"


def setup_logging() -> None:
    """Set up logging configuration."""
    os.makedirs(os.path.dirname(LOG_FILE_PATH), exist_ok=True)

    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    log_format = "[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s"
    date_format = "%Y-%m-%d %H:%M:%S"

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.handlers = []  # Reset handlers

    # Console Handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_formatter = ColoredFormatter(log_format, datefmt=date_format)
    console_handler.setFormatter(console_formatter)
    root_logger.addHandler(console_handler)

    # Rotating File Handler (Plain Text)
    file_handler = RotatingFileHandler(LOG_FILE_PATH, maxBytes=MAX_LOG_SIZE, backupCount=BACKUP_COUNT)
    file_formatter = logging.Formatter(log_format, datefmt=date_format)
    file_handler.setFormatter(file_formatter)
    root_logger.addHandler(file_handler)

    # JSON Logs (optional, useful for cloud logging systems)
    if settings.STRUCTURED_LOGGING:
        json_handler = logging.StreamHandler(sys.stdout)
        json_formatter = jsonlogger.JsonFormatter(
            fmt="%(asctime)s %(levelname)s %(name)s %(message)s",
            datefmt=date_format
        )
        json_handler.setFormatter(json_formatter)
        root_logger.addHandler(json_handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
