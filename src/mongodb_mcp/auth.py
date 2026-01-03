import os
import hmac
import hashlib
from functools import wraps
from mongodb_mcp.logging_config import get_logger

logger = get_logger("auth")

# Authentication modes
AUTH_DISABLED = "disabled"
AUTH_API_KEY = "api_key"
AUTH_BEARER = "bearer"

def get_auth_mode() -> str:
    """Get the configured authentication mode."""
    return os.getenv("AUTH_MODE", AUTH_DISABLED).lower()

def get_api_key() -> str | None:
    """Get the configured API key."""
    return os.getenv("MCP_API_KEY")

def validate_api_key(provided_key: str) -> bool:
    """Validate an API key using constant-time comparison."""
    expected_key = get_api_key()
    if not expected_key:
        logger.warning("API key validation requested but MCP_API_KEY not configured")
        return False
    
    # Use constant-time comparison to prevent timing attacks
    return hmac.compare_digest(provided_key, expected_key)

def require_auth(func):
    """Decorator to require authentication for a tool.
    
    This is a simple decorator that checks if auth is enabled.
    For HTTP transport, the actual auth header validation happens
    at the transport layer. This is for additional tool-level protection.
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth_mode = get_auth_mode()
        
        if auth_mode == AUTH_DISABLED:
            # No auth required
            return func(*args, **kwargs)
        
        # For tool-level auth, we log access
        # The actual auth validation happens at transport level
        logger.debug(f"Tool '{func.__name__}' called with auth mode: {auth_mode}")
        return func(*args, **kwargs)
    
    return wrapper

class AuthenticationError(Exception):
    """Raised when authentication fails."""
    pass
