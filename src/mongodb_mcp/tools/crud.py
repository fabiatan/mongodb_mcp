import json
import os
from mongodb_mcp.app import mcp
from mongodb_mcp.connection import get_client
from mongodb_mcp.logging_config import get_logger

logger = get_logger("tools.crud")

def _get_active_client():
    client = get_client()
    if not client:
        raise RuntimeError("Not connected to MongoDB. Please use 'connect' tool first.")
    return client

def _check_readonly():
    read_only = os.getenv("READ_ONLY", "false").lower() == "true"
    if read_only:
        logger.warning("Write operation blocked: server is in READ_ONLY mode")
        raise RuntimeError("Server is in READ-ONLY mode. Write operations are disabled.")

@mcp.tool()
def insert_one(database: str, collection: str, document: dict) -> str:
    """Insert a single document.
    
    Args:
        database: Database name
        collection: Collection name
        document: Document to insert
    """
    try:
        _check_readonly()
        client = _get_active_client()
        coll = client[database][collection]
        result = coll.insert_one(document)
        logger.info(f"insert_one: {database}.{collection} -> {result.inserted_id}")
        return json.dumps({"inserted_id": str(result.inserted_id)}, indent=2)
    except Exception as e:
        logger.error(f"insert_one failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def insert_many(database: str, collection: str, documents: list) -> str:
    """Insert multiple documents.
    
    Args:
        database: Database name
        collection: Collection name
        documents: List of documents to insert
    """
    try:
        _check_readonly()
        client = _get_active_client()
        coll = client[database][collection]
        result = coll.insert_many(documents)
        logger.info(f"insert_many: {database}.{collection} -> {len(result.inserted_ids)} docs")
        return json.dumps({
            "inserted_count": len(result.inserted_ids),
            "inserted_ids": [str(id) for id in result.inserted_ids]
        }, indent=2)
    except Exception as e:
        logger.error(f"insert_many failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def update_one(
    database: str, 
    collection: str, 
    filter: dict, 
    update: dict,
    upsert: bool = False
) -> str:
    """Update a single document.
    
    Args:
        database: Database name
        collection: Collection name
        filter: Filter to find document
        update: Update operations (e.g., {"$set": {"status": "active"}})
        upsert: If true, create a new document if no match found
    """
    try:
        _check_readonly()
        client = _get_active_client()
        coll = client[database][collection]
        result = coll.update_one(filter, update, upsert=upsert)
        logger.info(f"update_one: {database}.{collection} matched={result.matched_count} modified={result.modified_count}")
        return json.dumps({
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "upserted_id": str(result.upserted_id) if result.upserted_id else None
        }, indent=2)
    except Exception as e:
        logger.error(f"update_one failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def update_many(
    database: str, 
    collection: str, 
    filter: dict, 
    update: dict,
    upsert: bool = False
) -> str:
    """Update multiple documents.
    
    Args:
        database: Database name
        collection: Collection name
        filter: Filter to find documents
        update: Update operations
        upsert: If true, create if no match
    """
    try:
        _check_readonly()
        client = _get_active_client()
        coll = client[database][collection]
        result = coll.update_many(filter, update, upsert=upsert)
        logger.info(f"update_many: {database}.{collection} matched={result.matched_count} modified={result.modified_count}")
        return json.dumps({
            "matched_count": result.matched_count,
            "modified_count": result.modified_count,
            "upserted_id": str(result.upserted_id) if result.upserted_id else None
        }, indent=2)
    except Exception as e:
        logger.error(f"update_many failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def delete_one(database: str, collection: str, filter: dict) -> str:
    """Delete a single document.
    
    Args:
        database: Database name
        collection: Collection name
        filter: Filter to find document to delete
    """
    try:
        _check_readonly()
        client = _get_active_client()
        coll = client[database][collection]
        result = coll.delete_one(filter)
        logger.info(f"delete_one: {database}.{collection} deleted={result.deleted_count}")
        return json.dumps({"deleted_count": result.deleted_count}, indent=2)
    except Exception as e:
        logger.error(f"delete_one failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def delete_many(database: str, collection: str, filter: dict) -> str:
    """Delete multiple documents.
    
    Args:
        database: Database name
        collection: Collection name
        filter: Filter to find documents to delete
    """
    try:
        _check_readonly()
        client = _get_active_client()
        coll = client[database][collection]
        result = coll.delete_many(filter)
        logger.info(f"delete_many: {database}.{collection} deleted={result.deleted_count}")
        return json.dumps({"deleted_count": result.deleted_count}, indent=2)
    except Exception as e:
        logger.error(f"delete_many failed: {str(e)}")
        return f"Error: {str(e)}"
