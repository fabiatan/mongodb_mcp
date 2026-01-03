import logging
import sys
import os

def setup_logging():
    """Configure logging for the MCP server.
    
    MCP servers MUST NOT write to stdout (reserved for protocol).
    All logs go to stderr.
    """
    log_level = os.getenv("LOG_LEVEL", "INFO").upper()
    
    # Create formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    
    # Create stderr handler
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(getattr(logging, log_level, logging.INFO))
    root_logger.addHandler(handler)
    
    # Create a specific logger for our app
    logger = logging.getLogger("mongodb_mcp")
    logger.setLevel(getattr(logging, log_level, logging.INFO))
    
    return logger

# Initialize logger
logger = setup_logging()

def get_logger(name: str = None) -> logging.Logger:
    """Get a logger instance."""
    if name:
        return logging.getLogger(f"mongodb_mcp.{name}")
    return logging.getLogger("mongodb_mcp")
