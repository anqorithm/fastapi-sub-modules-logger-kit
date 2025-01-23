from typing import Any, Dict, Optional
from loguru import logger
import sys
import json
from pydantic import BaseModel

class LogConfig(BaseModel):
    """Logging configuration"""
    LOGGER_NAME: str = "fastapi_logger"
    LOG_FORMAT: str = "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
    LOG_LEVEL: str = "DEBUG"

    # Logging config
    version: int = 1
    disable_existing_loggers: bool = False
    formatters: Dict[str, Dict[str, str]] = {
        "default": {
            "()": "uvicorn.logging.DefaultFormatter",
            "fmt": LOG_FORMAT,
            "datefmt": "%Y-%m-%d %H:%M:%S",
        },
    }

class Logger:
    """Custom logger class"""
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._initialize_logger()
        return cls._instance

    def _initialize_logger(self):
        """Initialize logger with default configuration"""
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
            rotation="500 MB",
            retention="10 days",
            enqueue=True,
            backtrace=True,
            level=config.LOG_LEVEL,
            format=config.LOG_FORMAT,
        )

    @staticmethod
    def format_log_msg(msg: Any) -> str:
        """Format log message to string"""
        if isinstance(msg, (dict, list)):
            return json.dumps(msg, indent=2)
        return str(msg)

    def debug(self, msg: Any, **kwargs):
        """Debug level log"""
        logger.debug(self.format_log_msg(msg), **kwargs)

    def info(self, msg: Any, **kwargs):
        """Info level log"""
        logger.info(self.format_log_msg(msg), **kwargs)

    def warning(self, msg: Any, **kwargs):
        """Warning level log"""
        logger.warning(self.format_log_msg(msg), **kwargs)

    def error(self, msg: Any, **kwargs):
        """Error level log"""
        logger.error(self.format_log_msg(msg), **kwargs)

    def critical(self, msg: Any, **kwargs):
        """Critical level log"""
        logger.critical(self.format_log_msg(msg), **kwargs)

# Create a singleton instance
app_logger = Logger()
