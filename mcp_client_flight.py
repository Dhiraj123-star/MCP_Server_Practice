import asyncio
import os
import json
from datetime import timedelta
from datetime import datetime
from google import genai
from google.genai import types
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from dotenv import load_dotenv
load_dotenv()

# Get API keys from .env
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
SERP_API_KEY = os.getenv("SERP_API_KEY")

client = genai.Client(api_key=GEMINI_API_KEY)

# ✅ Ask user for input
source = input("Enter departure city (e.g., New Delhi): ").strip()
destination = input("Enter destination city (e.g., Mumbai): ").strip()
travel_date = input("Enter travel date (YYYY-MM-DD), or leave blank for tomorrow: ").strip()

# ✅ Use tomorrow's date if not provided
if not travel_date:
    travel_date = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")

# Set up the MCP tool to run
server_params = StdioServerParameters(
    command="mcp-flight-search",
    args=["--connection_type", "stdio"],
    env={"SERP_API_KEY": SERP_API_KEY},
)

async def run():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # ✅ Use dynamic prompt
            prompt = f"Find flights from {source} to {destination} on {travel_date}"

            mcp_tools = await session.list_tools()
            tools = [
                types.Tool(
                    function_declarations=[
                        {
                            "name": tool.name,
                            "description": tool.description,
                            "parameters": {
                                k: v
                                for k, v in tool.inputSchema.items()
                                if k not in ["additionalProperties", "$schema"]
                            },
                        }
                    ]
                )
                for tool in mcp_tools.tools
            ]

            # Ask Gemini to generate a response (or tool call)
            response = client.models.generate_content(
                model="gemini-2.5-pro-exp-03-25",
                contents=prompt,
                config=types.GenerateContentConfig(
                    temperature=0,
                    tools=tools,
                ),
            )

            # Handle tool use or fallback text
            if response.candidates[0].content.parts[0].function_call:
                function_call = response.candidates[0].content.parts[0].function_call

                result = await session.call_tool(
                    function_call.name, arguments=dict(function_call.args)
                )

                print("--- Formatted Result ---")
                try:
                    flight_data = json.loads(result.content[0].text)
                    print(json.dumps(flight_data, indent=2))
                except json.JSONDecodeError:
                    print("MCP server returned non-JSON response:")
                    print(result.content[0].text)
                except (IndexError, AttributeError):
                    print("Unexpected result structure from MCP server:")
                    print(result)
            else:
                print("No function call was generated by the model.")
                if response.text:
                    print("Model response:")
                    print(response.text)

# Run the async function
asyncio.run(run())
