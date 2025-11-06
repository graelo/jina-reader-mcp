import os
import logging
import tempfile
import atexit
import subprocess
import httpx
from fastmcp import FastMCP

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

mcp = FastMCP("jina-reader")

JINA_API_URL = os.getenv("JINA_API_URL", "http://localhost:8000").rstrip("/")
ROOT_CA_NAME = os.getenv("ROOT_CA_NAME", "").strip()


def get_internal_ca_pem(root_ca_name: str) -> str:
    """Extract internal root CA from System.keychain to a temp PEM file"""
    try:
        result = subprocess.run(
            [
                "security",
                "find-certificate",
                "-a",
                "-c",
                root_ca_name,
                "-p",
                "/System/Library/Keychains/System.keychain",
            ],
            capture_output=True,
            text=True,
            check=True,
        )
        temp = tempfile.NamedTemporaryFile(delete=False, suffix=".pem")
        temp.write(result.stdout.encode("utf-8"))
        temp.close()

        # ensure cleanup at process exit
        atexit.register(lambda: os.remove(temp.name))
        return temp.name
    except subprocess.CalledProcessError as e:
        logger.error(f"Failed to extract internal CA {root_ca_name}: {e}")
        raise


# decide if we need custom CA
if JINA_API_URL.lower().startswith("https") and ROOT_CA_NAME:
    VERIFY_PATH = get_internal_ca_pem(ROOT_CA_NAME)
else:
    VERIFY_PATH = True  # default verification


@mcp.tool
def read_url(url: str) -> str:
    """Extract clean content from a URL using self-hosted Jina Reader"""
    dest = f"{JINA_API_URL}/{url.lstrip('/')}"
    try:
        with httpx.Client(timeout=30.0, verify=VERIFY_PATH) as client:
            response = client.get(dest)
            response.raise_for_status()
            return response.text
    except Exception as e:
        logger.exception(f"Error fetching {url}")
        raise


def main():
    mcp.run()


if __name__ == "__main__":
    main()
