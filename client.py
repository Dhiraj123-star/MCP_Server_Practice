from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from langchain_mcp_adapters.tools import load_mcp_tools
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
import asyncio


model = ChatOpenAI(model="gpt-4o")

server_params = StdioServerParameters(
    command="python",
    # Make sure to update to the full absolute path to your math_server.py file
    args=["mcp_server.py"],
)

async def run_agent():
    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # Initialize the connection
            await session.initialize()

            # Get tools
            tools = await load_mcp_tools(session)

            # Create and run the agent
            agent = create_react_agent(model, tools)
            user_input=input("Enter your query:\n")
            agent_response = await agent.ainvoke({"messages": user_input})
            return agent_response

# Run the async function
if __name__ == "__main__":
    result = asyncio.run(run_agent())
    print(result)
    print("----------------------------------------------")
    print("Human Input---> ",result['messages'][0].content)
    print("AI response--->", getattr(result['messages'][1], 'content', 'None') if result['messages']=='' else 'None')
    print("AI Tool response -->", getattr(result['messages'][2], 'content', 'None') if len(result['messages']) > 2 else 'None')

    print("----------------------------------------------")
    


