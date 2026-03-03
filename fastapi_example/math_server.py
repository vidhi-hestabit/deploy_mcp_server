from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name="math",
    stateless_http=True
)

@mcp.tool(description="Add 2 to a number")
def add_two(n: int) -> int:
    return n + 2