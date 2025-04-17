# ./adk_agent_samples/mcp_agent/agent.py
import asyncio
from google.genai import types
from google.adk.agents.llm_agent import LlmAgent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from core.config import settings


# --- Step 1: Import Tools from MCP Server ---
async def get_tools_async():
    """Gets tools from the File System MCP Server."""
    print("Attempting to connect to MCP Filesystem server...")
    tools, exit_stack = await MCPToolset.from_server(
        connection_params=SseServerParams(url=settings.SSE_SERVER_PARAMS_URL)
    )
    print("MCP Toolset created successfully.")
    return tools, exit_stack


# --- Step 2: Agent Definition ---
async def get_agent_async():
    """Creates an ADK Agent equipped with tools from the MCP Server."""
    tools, exit_stack = await get_tools_async()
    print(f"Fetched {len(tools)} tools from MCP server.")
    
    root_agent = LlmAgent(
        model=settings.ADK_AGENT_MODEL,  # Adjust model name if needed based on availability
        name='html_parser',
        instruction='Fetch HTML from a URL, parse it, and convert the content to Markdown.',
        tools=tools,  # Provide the MCP tools to the ADK agent
    )
    return root_agent, exit_stack


# --- Step 3: Running the Agent ---
async def run_async_adkagent(query):
    session_service = InMemorySessionService()
 
    _app_name = 'adk_mcp_sample'

    session = session_service.create_session(
        state={}, app_name=_app_name, user_id='user_fs'
    )

    print("Session created successfully.")
    content = types.Content(role='user', parts=[types.Part(text=query)])

    root_agent, exit_stack = await get_agent_async()
    print("Agent created successfully.")
    runner = Runner(
        app_name=_app_name,
        agent=root_agent,
        session_service=session_service,
    )

    print("Running agent...")
    events_async = runner.run_async(
        session_id=session.id, user_id=session.user_id, new_message=content
    )

    final_response_text = ""

    async for event in events_async:
        if event.is_final_response():
            if event.content and event.content.parts:
                # Assuming text response in the first part
                for result in event.content.parts:
                    final_response_text += result.text
                    final_response_text += "\n"
            elif event.actions and event.actions.escalate:  # Handle potential errors/escalations
                final_response_text = f"Agent escalated: {event.error_message or 'No specific message.'}"
            break  # Stop processing events once the final response is found

    # Crucial Cleanup: Ensure the MCP server process connection is closed.
    print("Closing MCP server connection...")
    await exit_stack.aclose()
    print("Cleanup complete.")

    return final_response_text


# --- Step 4: Main Entry Point ---
if __name__ == '__main__':
    try:
        query = "https://github.com/Kewton/myaiagent の記事をマークダウン形式に変換して出力してください"
        final_response_text = asyncio.run(run_async_adkagent(query))
        print("=====   Final Response =====")
        print(final_response_text)

    except Exception as e:
        print(f"An error occurred: {e}")
