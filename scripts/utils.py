"""
PhilWeather ETL — Shared Utilities & Logging Module

Provides centralized logger setup with dual output (console stdout + pipeline.log)
and directory creation helpers.
"""

import logging
import sys
from pathlib import Path

# Ensure project root is in sys.path
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from scripts.config import get_settings

# Base log directory
LOG_DIR = Path(__file__).resolve().parent.parent / "data" / "logs"


def setup_logger(name: str = "philweather_etl") -> logging.Logger:
    """Configures and returns a logger with console and file handlers.

    Args:
        name (str): The name of the logger instance. Defaults to 'philweather_etl'.

    Returns:
        logging.Logger: Configured logger instance.
    """
    settings = get_settings()
    log_level = getattr(logging, settings.log_level.upper(), logging.INFO)

    logger = logging.getLogger(name)
    logger.setLevel(log_level)

    # Avoid attaching multiple handlers if logger is already initialized
    if logger.handlers:
        return logger

    # Ensure log directory exists
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    log_file_path = LOG_DIR / "pipeline.log"

    # Log format specification
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console Handler (stdout)
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File Handler
    file_handler = logging.FileHandler(log_file_path, encoding="utf-8")
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    return logger


def get_logger(name: str = "philweather_etl") -> logging.Logger:
    """Convenience helper to retrieve a configured logger instance.

    Args:
        name (str): Logger name. Defaults to 'philweather_etl'.

    Returns:
        logging.Logger: Logger instance.
    """
    return setup_logger(name)
