import argparse
import os
from mongodb_mcp.app import mcp
from mongodb_mcp.logging_config import get_logger

logger = get_logger("server")

def main():
    parser = argparse.ArgumentParser(description="MongoDB MCP Server")
    parser.add_argument(
        "--transport", 
        choices=["stdio", "streamable-http"], 
        default=os.getenv("MCP_TRANSPORT", "stdio"),
        help="Transport mode (default: stdio)"
    )
    parser.add_argument(
        "--host", 
        default=os.getenv("MCP_HOST", "0.0.0.0"),
        help="HTTP server bind address (default: 0.0.0.0)"
    )
    parser.add_argument(
        "--port", 
        type=int, 
        default=int(os.getenv("MCP_PORT", "8000")),
        help="HTTP server port (default: 8000)"
    )
    args = parser.parse_args()
    
    # Import tools to register them with the mcp instance
    # This must happen before mcp.run()
    logger.info("Registering tools...")
    from mongodb_mcp.tools import connection, exploration, query, crud
    
    logger.info(f"Starting MongoDB MCP Server")
    logger.info(f"Transport: {args.transport}")
    
    if args.transport == "streamable-http":
        logger.info(f"Listening on http://{args.host}:{args.port}")
        
        # Check auth configuration
        auth_mode = os.getenv("AUTH_MODE", "disabled")
        if auth_mode != "disabled":
            api_key = os.getenv("MCP_API_KEY")
            if not api_key:
                logger.warning("AUTH_MODE is enabled but MCP_API_KEY is not set!")
            else:
                logger.info(f"Authentication enabled: {auth_mode}")
        else:
            logger.warning("Authentication is DISABLED. Set AUTH_MODE and MCP_API_KEY for production.")
        
        mcp.run(transport="streamable-http", host=args.host, port=args.port)
    else:
        logger.info("Running in STDIO mode")
        mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
