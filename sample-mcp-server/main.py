from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv
from app.utils.html2markdown import getMarkdown
import os

load_dotenv()

HOST = os.getenv('HOST', "127.0.0.1")
PORT = os.getenv('PORT', 8001)

mcp = FastMCP("weather", host=HOST, port=PORT)


@mcp.tool()
async def getMarkdown_tool(url: str) -> str:
    """指定されたURLからHTMLを取得し、マークダウン形式に変換します。
    Args:
        url (str): 変換するURL。
    Returns:
        str: マークダウン形式に変換されたテキスト。
    """
    result = getMarkdown(url)

    if result["state"] == "success":
        print("Markdown conversion successful.")
        return result
    else:
        print("Markdown conversion failed.")
        return str(result["result"]) + "エラー"


if __name__ == "__main__":
    print("Starting weather MCP server...")
    mcp.run(transport='sse')