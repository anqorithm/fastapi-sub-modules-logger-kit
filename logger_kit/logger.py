"""Logger module for the application.

This module provides a custom logger implementation using loguru with singleton pattern
and configuration management through Pydantic models.
"""

from loguru import logger
import sys

from .config import LogConfig


class Logger:
    """A singleton logger class that provides logging functionality.
    
    This class implements a singleton pattern to ensure only one logger instance
    exists throughout the application. It uses loguru for logging and can be
    configured using Pydantic models.
    
    Attributes:
        _instance: The singleton instance of the logger.
    """
    
    _instance = None

    def __new__(cls):
        """Create a new Logger instance if one doesn't exist.
        
        Returns:
            Logger: The singleton instance of the Logger class.
        """
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """Initialize the logger with default configuration.
        
        This method sets up the logger with the configuration defined in LogConfig.
        It removes any existing handlers and adds new ones for stdout and file output.
        """
        config = LogConfig()

        # Remove default logger
        logger.remove()
        
        # Add new configuration
        logger.add(
            sys.stdout,
            enqueue=True,
            backtrace=True,
            level=config.LOG_LEVEL,
            format=config.LOG_FORMAT,
        )
        
        # Add file handler
        logger.add(
            "logs/app.log",
            rotation="10 MB",
            retention="1 week",
            enqueue=True,
            backtrace=True,
            level=config.LOG_LEVEL,
            format=config.LOG_FORMAT,
        )

    def debug(self, message):
        """Log a debug message.
        
        Args:
            message: The message to log at debug level.
        """
        logger.debug(message)

    def info(self, message):
        """Log an info message.
        
        Args:
            message: The message to log at info level.
        """
        logger.info(message)

    def warning(self, message):
        """Log a warning message.
        
        Args:
            message: The message to log at warning level.
        """
        logger.warning(message)

    def error(self, message):
        """Log an error message.
        
        Args:
            message: The message to log at error level.
        """
        logger.error(message)

    def critical(self, message):
        """Log a critical message.
        
        Args:
            message: The message to log at critical level.
        """
        logger.critical(message)


# Create a singleton instance
app_logger = Logger()
