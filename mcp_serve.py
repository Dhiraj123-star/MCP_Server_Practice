from mcp import ClientSession,StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
import asyncio
from langchain_google_genai import ChatGoogleGenerativeAI
import os
from dotenv import load_dotenv
load_dotenv()

gemini_api_key = os.getenv("GEMINI_API_KEY")

model = ChatGoogleGenerativeAI(
    model="gemini-2.0-flash-001",
    api_key =gemini_api_key,
)

server_params = StdioServerParameters(
    command="python",
    args=[
        "math_server.py"
    ]
)

async def run_agent():
    async with stdio_client(server_params) as (read,write):
        async with ClientSession(read,write) as session:
            # initialize the connection
            await session.initialize()

            # get tools
            tools = await load_mcp_tools(session)

            # create and run the agent 
            agent = create_react_agent(model,tools)
            user_query = input("Enter your query: ")
            agent_response = await agent.ainvoke({
                "messages":user_query
                }
            )
            return agent_response
        

# run the async function
if __name__=="__main__":
    try:
        result=asyncio.run(run_agent())
        print("Human Input---> ",result['messages'][0].content)
        print("AI Tool response -->", result['messages'][1].content)
    except:
        pass


