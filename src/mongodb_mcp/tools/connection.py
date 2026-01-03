import os
from pymongo import MongoClient
from mongodb_mcp.app import mcp
from mongodb_mcp.connection import set_client, get_client
from mongodb_mcp.logging_config import get_logger

logger = get_logger("tools.connection")

@mcp.tool()
def connect(connection_string: str = None) -> str:
    """Connect to a MongoDB instance.
    
    Args:
        connection_string: MongoDB URI. Uses MONGODB_URI env var if not provided.
    """
    uri = connection_string or os.getenv("MONGODB_URI")
    if not uri:
        return "Error: No connection string provided and MONGODB_URI not set in environment."
    
    # Mask the URI for logging (hide credentials)
    masked_uri = uri.split("@")[-1] if "@" in uri else uri
    logger.info(f"Connecting to MongoDB: ...@{masked_uri}")
    
    try:
        client = MongoClient(uri, serverSelectionTimeoutMS=5000)
        # Verify connection
        client.admin.command('ping')
        set_client(client)
        logger.info("Successfully connected to MongoDB")
        return "Successfully connected to MongoDB"
    except Exception as e:
        logger.error(f"Failed to connect: {str(e)}")
        set_client(None)
        return f"Failed to connect: {str(e)}"

@mcp.tool()
def disconnect() -> str:
    """Close the current MongoDB connection."""
    client = get_client()
    if client:
        client.close()
        set_client(None)
        logger.info("Disconnected from MongoDB")
        return "Disconnected from MongoDB."
    logger.debug("Disconnect called but no active connection")
    return "No active connection."

@mcp.tool()
def connection_status() -> str:
    """Check the current connection status."""
    client = get_client()
    if not client:
        return "Not connected."
    try:
        # Simple ping to check if connection is still alive
        client.admin.command('ping')
        logger.debug("Connection health check: OK")
        return "Connected and healthy."
    except Exception as e:
        logger.warning(f"Connection unhealthy: {str(e)}")
        return f"Connected but unhealthy: {str(e)}"
