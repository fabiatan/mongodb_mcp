FROM python:3.12-slim

WORKDIR /app

# Install uv for fast package management
RUN pip install uv

# Copy project files
COPY pyproject.toml .
COPY src/ src/
COPY README.md .

# Install dependencies
RUN uv pip install --system -e .

# Expose HTTP port
EXPOSE 8000

# Health check endpoint
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Run with Streamable HTTP transport
CMD ["python", "-m", "mongodb_mcp.server", "--transport", "streamable-http", "--host", "0.0.0.0", "--port", "8000"]
