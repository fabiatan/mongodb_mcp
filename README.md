# MongoDB MCP Server

A generic Model Context Protocol (MCP) server for MongoDB that allows MCP hosts (Claude Desktop, Cursor, etc.) to interact with MongoDB databases using natural language.

## Features

- **Connection Management**: Connect to any MongoDB instance
- **Database Exploration**: List databases, collections, infer schemas
- **Query Operations**: find, find_one, aggregate, count, distinct
- **CRUD Operations**: insert, update, delete (with READ_ONLY mode support)
- **Authentication**: Optional API key authentication
- **Logging**: Structured logging to stderr
- **Docker Support**: Ready for containerized deployment

## Quick Start

### Local Development

```bash
# Install dependencies
pip install uv
uv sync

# Run in STDIO mode (for local MCP hosts)
uv run python -m mongodb_mcp.server

# Run in HTTP mode (for remote access)
uv run python -m mongodb_mcp.server --transport streamable-http --port 8000
```

### Docker

```bash
# Copy and configure environment
cp .env.example .env
# Edit .env with your settings

# Build and run
docker compose up --build -d

# Server available at http://localhost:8000
```

## Configuration

All configuration is done via environment variables (see `.env.example`):

| Variable | Description | Default |
|----------|-------------|---------|
| `MONGODB_URI` | MongoDB connection string | `mongodb://localhost:27017` |
| `MONGODB_DEFAULT_DB` | Default database | - |
| `READ_ONLY` | Disable write operations | `false` |
| `MAX_DOCUMENTS` | Max documents returned | `100` |
| `LOG_LEVEL` | Logging level (DEBUG/INFO/WARNING/ERROR) | `INFO` |
| `AUTH_MODE` | Authentication mode (`disabled`/`api_key`) | `disabled` |
| `MCP_API_KEY` | API key for authentication | - |

## MCP Host Configuration

### Claude Desktop / Cursor (Local STDIO)

```json
{
  "mcpServers": {
    "mongodb": {
      "command": "uv",
      "args": ["run", "--directory", "/path/to/mongodb_mcp", "python", "-m", "mongodb_mcp.server"]
    }
  }
}
```

### Remote HTTP

```json
{
  "mcpServers": {
    "mongodb": {
      "url": "http://your-server:8000/mcp"
    }
  }
}
```

## Available Tools

| Tool | Description |
|------|-------------|
| `connect` | Connect to MongoDB instance |
| `disconnect` | Close connection |
| `connection_status` | Check connection health |
| `list_databases` | List all databases |
| `list_collections` | List collections in a database |
| `collection_schema` | Infer schema from samples |
| `collection_stats` | Get collection statistics |
| `find` | Query documents |
| `find_one` | Find single document |
| `count` | Count documents |
| `distinct` | Get distinct field values |
| `aggregate` | Run aggregation pipeline |
| `insert_one` | Insert single document |
| `insert_many` | Insert multiple documents |
| `update_one` | Update single document |
| `update_many` | Update multiple documents |
| `delete_one` | Delete single document |
| `delete_many` | Delete multiple documents |

## License

MIT
