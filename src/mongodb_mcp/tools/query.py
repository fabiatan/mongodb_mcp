import json
import os
from mongodb_mcp.app import mcp
from mongodb_mcp.connection import get_client
from mongodb_mcp.logging_config import get_logger
from bson import json_util

logger = get_logger("tools.query")

def _get_active_client():
    client = get_client()
    if not client:
        raise RuntimeError("Not connected to MongoDB. Please use 'connect' tool first.")
    return client

def _serialize(data):
    """Serialize MongoDB data to JSON using json_util to handle ObjectIds etc."""
    return json.loads(json_util.dumps(data))

@mcp.tool()
def find(
    database: str,
    collection: str,
    filter: dict = None,
    projection: dict = None,
    sort: dict = None,
    limit: int = 20
) -> str:
    """Query documents from a MongoDB collection.
    
    Args:
        database: Database name
        collection: Collection name
        filter: Query filter (MongoDB filter syntax)
        projection: Fields to include/exclude (e.g., {"name": 1, "_id": 0})
        sort: Sort order (e.g., {"created_at": -1})
        limit: Maximum documents to return (default: 20)
    """
    try:
        client = _get_active_client()
        
        max_docs = int(os.getenv("MAX_DOCUMENTS", "100"))
        limit = min(limit, max_docs)
        
        logger.info(f"find: {database}.{collection} filter={filter} limit={limit}")
        
        coll = client[database][collection]
        cursor = coll.find(filter or {}, projection or {})
        
        if sort:
            cursor = cursor.sort(list(sort.items()))
        
        cursor = cursor.limit(limit)
        documents = list(cursor)
        
        logger.info(f"find: returned {len(documents)} documents")
        
        return json.dumps({
            "count": len(documents), 
            "documents": _serialize(documents)
        }, indent=2)
        
    except Exception as e:
        logger.error(f"find failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def find_one(
    database: str,
    collection: str,
    filter: dict = None,
    projection: dict = None
) -> str:
    """Find a single document matching criteria.
    
    Args:
        database: Database name
        collection: Collection name
        filter: Query filter
        projection: Fields to include/exclude
    """
    try:
        client = _get_active_client()
        logger.info(f"find_one: {database}.{collection} filter={filter}")
        
        coll = client[database][collection]
        document = coll.find_one(filter or {}, projection or {})
        
        if not document:
            logger.debug("find_one: no document found")
            return "No document found."
            
        return json.dumps(_serialize(document), indent=2)
        
    except Exception as e:
        logger.error(f"find_one failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def count(
    database: str,
    collection: str,
    filter: dict = None
) -> str:
    """Count documents matching a filter.
    
    Args:
        database: Database name
        collection: Collection name
        filter: Query filter
    """
    try:
        client = _get_active_client()
        coll = client[database][collection]
        count_val = coll.count_documents(filter or {})
        logger.info(f"count: {database}.{collection} = {count_val}")
        return json.dumps({"count": count_val}, indent=2)
    except Exception as e:
        logger.error(f"count failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def distinct(
    database: str,
    collection: str,
    field: str,
    filter: dict = None
) -> str:
    """Get distinct values for a field.
    
    Args:
        database: Database name
        collection: Collection name
        field: Field name to get distinct values for
        filter: Optional query filter
    """
    try:
        client = _get_active_client()
        coll = client[database][collection]
        values = coll.distinct(field, filter or {})
        logger.info(f"distinct: {database}.{collection}.{field} = {len(values)} values")
        return json.dumps({"values": _serialize(values)}, indent=2)
    except Exception as e:
        logger.error(f"distinct failed: {str(e)}")
        return f"Error: {str(e)}"

@mcp.tool()
def aggregate(
    database: str,
    collection: str,
    pipeline: list
) -> str:
    """Run an aggregation pipeline.
    
    Args:
        database: Database name
        collection: Collection name
        pipeline: Aggregation pipeline stages
    """
    try:
        client = _get_active_client()
        
        read_only = os.getenv("READ_ONLY", "false").lower() == "true"
        if read_only:
            str_pipeline = str(pipeline)
            if "$out" in str_pipeline or "$merge" in str_pipeline:
                logger.warning("Blocked aggregation with $out/$merge in read-only mode")
                return "Error: Aggregation with $out or $merge is not allowed in read-only mode."

        max_docs = int(os.getenv("MAX_DOCUMENTS", "100"))
        
        logger.info(f"aggregate: {database}.{collection} pipeline={len(pipeline)} stages")
        
        coll = client[database][collection]
        cursor = coll.aggregate(pipeline)
        
        documents = []
        for doc in cursor:
            documents.append(doc)
            if len(documents) >= max_docs:
                break
        
        logger.info(f"aggregate: returned {len(documents)} documents")
                
        return json.dumps({
            "count": len(documents), 
            "documents": _serialize(documents)
        }, indent=2)
        
    except Exception as e:
        logger.error(f"aggregate failed: {str(e)}")
        return f"Error: {str(e)}"
