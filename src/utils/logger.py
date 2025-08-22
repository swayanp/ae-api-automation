"""
logger.py
----------
This file defines a reusable logging function for the entire framework.

Features:
- Logs to both console and file (logs/run.log)
- Auto-creates the logs/ folder if missing
- Applies consistent log format: time | level | logger name | message
- Uses rotating file handler to limit log size (2MB, 3 backups)
- Prevents duplicate logs when used across multiple modules
"""

import logging
import os
from logging.handlers import RotatingFileHandler

def get_logger(name: str) -> logging.Logger:
    """
    Creates and returns a configured logger with console + file output.

    Args:
        name (str): Name of the logger (usually the module or file name)

    Returns:
        logging.Logger: The configured logger object
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger  # prevents adding duplicate handlers if logger already set up
    
    logger.setLevel(logging.INFO)
    os.makedirs("logs", exist_ok=True)

    # File handler with rotation (2 MB per file, keep 3 old backups)
    file_handler = RotatingFileHandler(
        "logs/run.log", maxBytes=2_000_000, backupCount=3
    )

    # Stream handler = logs to console
    console_handler = logging.StreamHandler()

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)
   
    # Attach both handlers to the logger
    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger



