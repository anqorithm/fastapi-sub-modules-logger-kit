"""Configuration module for the logger kit.

This module contains the Pydantic models for configuring the logging system.
"""

from pydantic import BaseModel


class LogConfig(BaseModel):
    """Configuration class for logging settings.
    
    This class defines all the configuration parameters needed for the logging system,
    including format strings, log levels, and logging handlers configuration.
    
    Attributes:
        LOGGER_NAME: The name of the logger instance.
        LOG_FORMAT: The format string for log messages.
        LOG_LEVEL: The minimum logging level to capture.
        version: The logging configuration version.
        disable_existing_loggers: Whether to disable existing logger instances.
        formatters: Dictionary containing formatter configurations.
    """
    
    LOGGER_NAME = "fastapi_logger"
    LOG_FORMAT = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    LOG_LEVEL = "DEBUG"

    # Logging config
    version = 1
    disable_existing_loggers = False
    formatters = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }
