import json
from mongodb_mcp.app import mcp
from mongodb_mcp.connection import get_client
from mongodb_mcp.logging_config import get_logger

logger = get_logger("tools.exploration")

def _get_active_client():
    client = get_client()
    if not client:
        raise RuntimeError("Not connected to MongoDB. Please use 'connect' tool first.")
    return client

@mcp.tool()
def list_databases() -> str:
    """List all databases on the connected MongoDB instance."""
    try:
        client = _get_active_client()
        databases = client.list_database_names()
        logger.info(f"Listed {len(databases)} databases")
        return json.dumps({"databases": databases}, indent=2)
    except Exception as e:
        logger.error(f"list_databases failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def list_collections(database: str) -> str:
    """List collections in a specified database.
    
    Args:
        database: database name
    """
    try:
        client = _get_active_client()
        db = client[database]
        collections = db.list_collection_names()
        logger.info(f"Listed {len(collections)} collections in '{database}'")
        return json.dumps({"database": database, "collections": collections}, indent=2)
    except Exception as e:
        logger.error(f"list_collections failed for '{database}': {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def collection_stats(database: str, collection: str) -> str:
    """Get statistics for a collection (count, size, avg object size).
    
    Args:
        database: Database name
        collection: Collection name
    """
    try:
        client = _get_active_client()
        db = client[database]
        stats = db.command("collStats", collection)
        
        relevant_stats = {
            "ns": stats.get("ns"),
            "count": stats.get("count"),
            "size": stats.get("size"),
            "avgObjSize": stats.get("avgObjSize"),
            "storageSize": stats.get("storageSize"),
            "nindexes": stats.get("nindexes"),
            "totalIndexSize": stats.get("totalIndexSize")
        }
        logger.info(f"Retrieved stats for '{database}.{collection}': {relevant_stats.get('count')} docs")
        return json.dumps(relevant_stats, indent=2)
    except Exception as e:
        logger.error(f"collection_stats failed for '{database}.{collection}': {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def collection_schema(database: str, collection: str, sample_size: int = 5) -> str:
    """Infer a simple schema from sample documents.
    
    Args:
        database: Database name
        collection: Collection name
        sample_size: Number of documents to sample (default: 5)
    """
    try:
        client = _get_active_client()
        coll = client[database][collection]
        
        cursor = coll.aggregate([{"$sample": {"size": sample_size}}])
        samples = list(cursor)
        
        if not samples:
            logger.info(f"Collection '{database}.{collection}' is empty")
            return "Collection is empty, cannot infer schema."
            
        schema_keys = {}
        for doc in samples:
            for key, value in doc.items():
                type_name = type(value).__name__
                if key not in schema_keys:
                    schema_keys[key] = set()
                schema_keys[key].add(type_name)
        
        final_schema = {k: list(v) for k, v in schema_keys.items()}
        logger.info(f"Inferred schema for '{database}.{collection}' from {len(samples)} samples")
        
        return json.dumps({
            "database": database,
            "collection": collection,
            "sampled_docs": len(samples),
            "inferred_schema": final_schema
        }, indent=2)
        
    except Exception as e:
        logger.error(f"collection_schema failed for '{database}.{collection}': {str(e)}")
        return f"Error: {str(e)}"
