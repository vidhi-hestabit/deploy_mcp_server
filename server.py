from typing import Dict, List
from mcp.server.fastmcp import FastMCP
from tavily import TavilyClient
from dotenv import load_dotenv
import os
import os

load_dotenv()
if "TAVILY_API_KEY" not in os.environ:
    raise ValueError("TAVILY_API_KEY is not set")

TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
tavily_client = TavilyClient(api_key=TAVILY_API_KEY)

mcp = FastMCP("web_search", host="0.0.0.0", port=8000)

@mcp.tool()
def web_search(query: str) -> List[Dict]:
    """Use this tool to search the web for information using the Tavily API.

    Args:
        query: The search query to use.
    
    Returns:
        The search results.
    """
    try:
        response=tavily_client.search(query)
        return response["results"]
    except Exception as e:
        raise Exception(f"Error searching the web: {e}")

if __name__ == "__main__":
    mcp.run(transport="streamable-http")