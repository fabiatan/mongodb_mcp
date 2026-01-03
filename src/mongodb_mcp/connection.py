from pymongo import MongoClient
from typing import Optional

_client: Optional[MongoClient] = None

def get_client() -> Optional[MongoClient]:
    return _client

def set_client(client: Optional[MongoClient]):
    global _client
    _client = client
