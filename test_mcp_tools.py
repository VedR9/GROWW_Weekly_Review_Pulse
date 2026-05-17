import asyncio
import sys
import logging
from mcp.client.sse import sse_client
from mcp.client.session import ClientSession

logging.basicConfig(level=logging.INFO)

import os

async def run():
    url = os.getenv("MCP_SERVER_URL", "https://your-mcp-server.onrender.com") + "/sse"
    print(f"Connecting to {url}")
    
    try:
        async with sse_client(url) as streams:
            async with ClientSession(streams[0], streams[1]) as session:
                await session.initialize()
                print("Session initialized!")
                
                tools = await session.list_tools()
                print("\nAvailable tools:")
                for tool in tools.tools:
                    print(f"- {tool.name}: {tool.description}")
                    for prop_name, prop in tool.inputSchema.get('properties', {}).items():
                        print(f"  * {prop_name}: {prop.get('description', '')}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(run())
