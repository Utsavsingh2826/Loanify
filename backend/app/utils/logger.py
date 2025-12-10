"""Structured logging configuration."""
import structlog
import logging
import sys
from typing import Any, Dict


def setup_logging(debug: bool = False) -> None:
    """Set up structured logging."""
    
    log_level = logging.DEBUG if debug else logging.INFO
    
    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=log_level,
    )
    
    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.processors.add_log_level,
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.dev.ConsoleRenderer() if debug else structlog.processors.JSONRenderer()
        ],
        wrapper_class=structlog.make_filtering_bound_logger(log_level),
        context_class=dict,
        logger_factory=structlog.PrintLoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str) -> Any:
    """Get a structured logger instance."""
    return structlog.get_logger(name)


def log_audit_event(
    event_type: str,
    user_id: str,
    details: Dict[str, Any],
    logger: Any = None
) -> None:
    """Log an audit event."""
    if logger is None:
        logger = get_logger("audit")
    
    logger.info(
        "audit_event",
        event_type=event_type,
        user_id=user_id,
        **details
    )


