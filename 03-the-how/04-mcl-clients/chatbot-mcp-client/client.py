import asyncio
from langchain_mcp_adapters.client import MultiServerMCPClient
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain_core.messages import ToolMessage
import json
import os 


load_dotenv()

SERVERS = { 
    "math": {
        "transport": "stdio",
        "command": "C:/Users/Asus/.local/bin/uv.exe",
        "args": [
            "run",
            "fastmcp",
            "run",
            "V:/Project Eagle/mcp-playground/03-the-how/04-mcl-clients/mcp-math-server/main.py",
        ],
    },
    "expense": {
        "transport": "streamable_http", 
        "url": "https://expence-tracker-mcp-vbp.fastmcp.app/mcp"
        
    },
    "manim-server": {
        "transport": "stdio",
        "command": "E:/claud-testing/manim-env/Scripts/python.exe",
        "args": ["E:/claud-testing/manim-mcp-server/src/manim_server.py"],
        "env": {
        "MANIM_EXECUTABLE": "E:/claud-testing/manim-env/Scripts/manim.exe"
        },
    }
}

async def main():
    
    client = MultiServerMCPClient(SERVERS)
    tools = await client.get_tools()


    named_tools = {}
    for tool in tools:
        named_tools[tool.name] = tool

    print("Available tools:", named_tools.keys())

    llm  = ChatOpenAI(
        model="openai/gpt-oss-20b",
        api_key=os.getenv("GROQ_API_KEY"),
        base_url= os.getenv("GROQ_BASE_URL"),
        max_tokens=300,
        temperature=0.5
    )
    llm_with_tools = llm.bind_tools(tools)

    prompt = "Draw a triangle rotating in place using the manim tool."
    response = await llm_with_tools.ainvoke(prompt)

    if not getattr(response, "tool_calls", None):
        print("\nLLM Reply:", response.content)
        return

    tool_messages = []
    for tc in response.tool_calls:
        selected_tool = tc["name"]
        selected_tool_args = tc.get("args") or {}
        selected_tool_id = tc["id"]

        result = await named_tools[selected_tool].ainvoke(selected_tool_args)
        tool_messages.append(ToolMessage(tool_call_id=selected_tool_id, content=json.dumps(result)))
        

    final_response = await llm_with_tools.ainvoke([prompt, response, *tool_messages])
    print(f"Final response: {final_response.content}")


if __name__ == '__main__':
    asyncio.run(main())