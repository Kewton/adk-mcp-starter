# graph.py
from contextlib import asynccontextmanager
from langchain_mcp_adapters.client import MultiServerMCPClient
from langgraph.prebuilt import create_react_agent
from langchain_openai import ChatOpenAI
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.messages.tool import ToolMessage
from dotenv import load_dotenv
import asyncio
import os
import json

load_dotenv()

SSE_SERVER_PARAMS_URL = os.getenv('SSE_SERVER_PARAMS_URL', "http://localhost:8001/sse")

model = ChatOpenAI(model="gpt-4o-mini")


# Make the graph with MCP context
@asynccontextmanager
async def make_graph():
    mcp_client = MultiServerMCPClient(
        {
            "my-mcp-tool": {
                "url": SSE_SERVER_PARAMS_URL,
                "transport": "sse",
            }
        }
    )

    async with mcp_client:
        mcp_tools = mcp_client.get_tools()
        print(f"Available tools: {[tool.name for tool in mcp_tools]}")
        graph = create_react_agent(model, mcp_client.get_tools())

        # graph = graph_builder.compile()
        graph.name = "Tool Agent"

        yield graph


# Run the graph with question
async def main(query):
    async with make_graph() as graph:
        result = await graph.ainvoke({"messages": query})
        # 1. 'messages' キーでメッセージリストを取得
        message_list = result.get('messages', []) # .get() を使うとキーが存在しない場合もエラーにならない

        # 2. リストが空でないことを確認し、最後のメッセージを取得
        final_output = {}
        humanMessage = ""
        aiMessage = ""
        toolMessages = []
        for message in message_list:
            print("~~~~")
            if isinstance(message, AIMessage):
                aiMessage = message.content
            elif isinstance(message, HumanMessage):
                humanMessage = message.content
            elif isinstance(message, ToolMessage):
                toolMessage = json.loads(message.content)
                toolMessages.append(
                    {
                        "state": toolMessage["state"],
                        "name": message.name,
                        "id": message.id,
                        "tool_call_id": message.tool_call_id,
                        "result": toolMessage["result"]
                    }
                )
            else:
                print("Unknown message type:", type(message))
                print(message)

        final_output = {
            "humanMessage": humanMessage,
            "aiMessage": aiMessage,
            "toolMessages": toolMessages
        }
        #     # 3. 最後のメッセージの内容 (content) を取得
        #     #    通常、最終応答は AIMessage のことが多い
        #     if isinstance(last_message, AIMessage):
        #         final_output = last_message.content
        #         print("最終的なアウトプット:", final_output)
        #     else:
        #         # 最後のメッセージがAIMessageでない場合（エラーなど）の処理
        #         print("最後のメッセージはAIの応答ではありませんでした:", last_message)
        #         final_output = last_message # または None やエラー処理
        # else:
        #     # メッセージリストが空だった場合の処理
        #     print("結果にメッセージリストが含まれていませんでした。")
        #     final_output = None
        
        return final_output


if __name__ == '__main__':
    try:
        query = "https://github.com/Kewton/myaiagent の記事をマークダウン形式に変換して出力してください"
        final_output = asyncio.run(main(query))
        print("=====   Final Response =====")
        print(final_output["humanMessage"])
        print(final_output["aiMessage"])
        print("=====   Tool Messages =====")
        for toolMessage in final_output["toolMessages"]:
            print(f"Tool Name: {toolMessage['name']}")
            print(f"State: {toolMessage['state']}")
            print(f"ID: {toolMessage['id']}")
            print(f"Tool Call ID: {toolMessage['tool_call_id']}")
            print(f"Result: {toolMessage['result']}")
            print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~")

    except Exception as e:
        print(f"An error occurred: {e}")