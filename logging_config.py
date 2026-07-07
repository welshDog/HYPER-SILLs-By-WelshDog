"""
Structured logging configuration for HYPER-SILLs MCP Server.
Provides JSON-formatted logs for better observability in Railway.
"""

import json
import logging
import sys
from datetime import datetime
from typing import Any


class JSONFormatter(logging.Formatter):
    """Format logs as JSON for structured logging in Railway."""

    def format(self, record: logging.LogRecord) -> str:
        log_data = {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
            "module": record.module,
            "function": record.funcName,
            "line": record.lineno,
        }

        # Add exception info if present
        if record.exc_info:
            log_data["exception"] = self.formatException(record.exc_info)

        # Add custom fields if present
        if hasattr(record, "extra_fields"):
            log_data.update(record.extra_fields)

        return json.dumps(log_data, ensure_ascii=False)


def setup_logging(level: int = logging.INFO) -> None:
    """Configure structured JSON logging for Railway."""
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    # Remove existing handlers
    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    # Add JSON formatter to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)

    # Suppress noisy libraries
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("uvicorn.error").setLevel(logging.WARNING)
    logging.getLogger("httpx").setLevel(logging.WARNING)


def get_logger(name: str) -> logging.LoggerAdapter:
    """Get a logger with support for extra fields."""
    logger = logging.getLogger(name)
    return logging.LoggerAdapter(logger, {})


class StructuredLogger:
    """Helper for adding structured fields to logs."""

    def __init__(self, logger: logging.Logger):
        self.logger = logger

    def info(self, message: str, **fields: Any) -> None:
        """Log info with structured fields."""
        extra = {"extra_fields": fields} if fields else {}
        self.logger.info(message, extra=extra)

    def error(self, message: str, **fields: Any) -> None:
        """Log error with structured fields."""
        extra = {"extra_fields": fields} if fields else {}
        self.logger.error(message, extra=extra)

    def warning(self, message: str, **fields: Any) -> None:
        """Log warning with structured fields."""
        extra = {"extra_fields": fields} if fields else {}
        self.logger.warning(message, extra=extra)

    def debug(self, message: str, **fields: Any) -> None:
        """Log debug with structured fields."""
        extra = {"extra_fields": fields} if fields else {}
        self.logger.debug(message, extra=extra)

