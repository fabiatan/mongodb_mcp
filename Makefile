.PHONY: help install dev run run-http docker-up docker-down docker-logs clean

help:
@echo "MongoDB MCP Server"
@echo ""
@echo "Usage:"
@echo "  make install      Install dependencies"
@echo "  make dev          Run MCP Inspector for development"
@echo "  make run          Run server (STDIO mode)"
@echo "  make run-http     Run server (HTTP mode)"
@echo "  make docker-up    Start Docker containers"
@echo "  make docker-down  Stop Docker containers"
@echo "  make docker-logs  View Docker logs"
@echo "  make clean        Remove cache files"

install:
pip install uv
uv sync

dev:
uv run mcp dev src/mongodb_mcp/server.py

run:
uv run python -m mongodb_mcp.server

run-http:
uv run python -m mongodb_mcp.server --transport streamable-http

docker-up:
docker compose up --build -d

docker-down:
docker compose down

docker-logs:
docker compose logs -f mongodb-mcp

clean:
find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete 2>/dev/null || true
rm -rf .pytest_cache .coverage htmlcov dist build *.egg-info
