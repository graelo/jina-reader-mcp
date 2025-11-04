import os
import logging
from fastmcp import FastMCP
import httpx

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mcp = FastMCP("jina-reader")

JINA_API_URL = os.getenv("JINA_API_URL", "http://localhost:8000").rstrip("/")


@mcp.tool
def read_url(url: str) -> str:
    """Extract clean content from a URL using self-hosted Jina Reader"""
    url = url.lstrip("/")
    dest = f"{JINA_API_URL}/{url}"

    try:
        with httpx.Client(timeout=30.0, verify=False) as client:
            response = client.get(dest)
            response.raise_for_status()
            return response.text
    except Exception as e:
        logger.error(f"Error fetching {url}: {e}", exc_info=True)
        raise


def main():
    mcp.run()


if __name__ == "__main__":
    main()
