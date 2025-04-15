from mcp.server.fastmcp import FastMCP

mcp=FastMCP("Math")

def add(a:int,b:int)-> int:
    """Add two numbers"""
    return a+b

def multiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b

if __name__=="__main__":
    mcp.run(transport="stdio")

    