from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo Server")

# define a tool function

@mcp.tool()
def multiply(a:int,b:int)-> int:
    """Multiply two numbers"""
    return a*b

# define resource function
@mcp.resource("greeting://{name}")
def get_greeting(name:str)->str:
    """Get a message for the given name."""
    return f"{name} is using MCP server!!!"

