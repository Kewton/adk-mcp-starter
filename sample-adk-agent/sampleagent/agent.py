from common.base import McpAgentToolAgent
import os


SSE_SERVER_PARAMS_URL = os.getenv('SSE_SERVER_PARAMS_URL', "http://localhost:8001/sse")
MODEL = os.getenv('MODEL', "gemini-1.5-flash")  # Adjust this to your desired model


root_agent = McpAgentToolAgent(
    model=MODEL,  # Adjust model name if needed based on availability
    name='html_parser',
    instruction='Fetch HTML from a URL, parse it, and convert the content to Markdown.',
    tools=[],  # Provide the MCP tools to the ADK agent
    mcp_server_url=SSE_SERVER_PARAMS_URL,  # URL to the MCP server
)