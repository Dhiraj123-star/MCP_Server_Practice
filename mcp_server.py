from mcp.server.fastmcp import FastMCP
import openai
import os

from dotenv import load_dotenv

load_dotenv()

mcp = FastMCP("MCP_Server")


client = openai.OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@mcp.tool()
def add(a:int,b:int)->int:
    """Add two numbers"""
    return a+b

@mcp.tool()
def multiply(a:int,b:int)->int:
    """Multiply two numbers"""
    return a*b

@mcp.tool()
def web_search(key_term: str) -> str:
    """
    Perform a web search using the Responses API and return the result.
    """
    # Simulated client.responses.create logic for web search
    response = client.responses.create(
        model="gpt-4o-mini",
        instructions="Web search for the latest information and give me a concise summary",
        input=key_term,
        tools=[{
            "type": "web_search_preview",
            "search_context_size": "medium",
        }],
        max_output_tokens=100  # Limit token usage for faster responses
    )
    return response.output_text

if __name__=="__main__":
    mcp.run(transport="stdio")

