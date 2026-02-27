"""
Logging configuration for Cognitive Twin
"""

import logging
import sys
from datetime import datetime

# Create logger
logger = logging.getLogger("cognitive_twin")
logger.setLevel(logging.DEBUG)

# Console handler
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)

# Formatter
formatter = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
handler.setFormatter(formatter)

# Add handler to logger
logger.addHandler(handler)


def get_logger(name: str):
    """Get a logger instance"""
    return logging.getLogger(f"cognitive_twin.{name}")


def log_request(method: str, path: str, user_id: int = None):
    """Log incoming request"""
    user_str = f" [User: {user_id}]" if user_id else ""
    logger.info(f"→ {method} {path}{user_str}")


def log_response(method: str, path: str, status_code: int, user_id: int = None):
    """Log outgoing response"""
    user_str = f" [User: {user_id}]" if user_id else ""
    logger.info(f"← {method} {path} {status_code}{user_str}")


def log_error(error_name: str, message: str, user_id: int = None):
    """Log error"""
    user_str = f" [User: {user_id}]" if user_id else ""
    logger.error(f"❌ {error_name}: {message}{user_str}")
