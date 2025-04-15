from google.adk.agents.llm_agent import (
    LlmAgent,
    InvocationContext,
    Event,
)
from google.adk.tools.mcp_tool.mcp_toolset import MCPToolset, SseServerParams
from typing import AsyncGenerator, Optional
from typing_extensions import override
from contextlib import AsyncExitStack


class McpAgentToolAgent(LlmAgent):

    # インスタンスごとにMCPサーバーのURLを保持する変数
    mcp_server_url: str

    @override
    async def _run_async_impl(
        self, ctx: InvocationContext
    ) -> AsyncGenerator[Event, None]:
        """
        MCPサーバーから動的にツールを取得し、コアロジックを実行後、リソースをクリーンアップします。
        """
        print(f"Agent '{self.name}': Entering custom _run_async_impl.")

        original_tools = list(self.tools)  # 元のツールをコピーして保持 (変更される可能性があるため)
        exit_stack: Optional[AsyncExitStack] = None  # exit_stackを初期化

        try:
            # 1. MCPサーバーからツールとExitStackを取得
            print(f"Agent '{self.name}': Fetching tools from MCP server ({self.mcp_server_url})...")

            # MCPToolset.from_server は接続を確立し、クリーンアップ用の exit_stack を返す
            tools, exit_stack = await MCPToolset.from_server(
                connection_params=SseServerParams(url=self.mcp_server_url)
            )
            self.tools = tools  # この実行のためにツールを再設定
            tool_names = [getattr(t, 'name', str(t)) for t in self.tools]  # 安全に名前を取得
            print(f"Agent '{self.name}': Tools reconfigured to: {tool_names}")

            # 2. 親クラスのコアロジックを実行 (新しいツールが使われる)
            print(f"Agent '{self.name}': Calling super()._run_async_impl to process request...")
            async for event in super()._run_async_impl(ctx):
                yield event
            print(f"Agent '{self.name}': Finished processing request in super()._run_async_impl.")

        except Exception as e:
            print(f"Agent '{self.name}': Error during execution: {e}", exc_info=True)
            # エラー発生時は元のツールに戻す (オプション)
            self.tools = original_tools
            print(f"Agent '{self.name}': Reverted to original tools due to error.")
            # エラーを再raiseするか、エラーイベントをyieldするかなどを検討
            # raise e # エラーを呼び出し元に伝える場合
        finally:
            # 3. 取得したexit_stackをクローズしてリソースを解放
            print(f"Agent '{self.name}': Entering finally block for cleanup.")
            if exit_stack:
                print(f"Agent '{self.name}': Closing MCP toolset exit_stack...")
                try:
                    await exit_stack.aclose()
                    print(f"Agent '{self.name}': MCP toolset exit_stack closed successfully.")
                except Exception as close_exc:
                    # クリーンアップ中のエラーもログに残す
                    print(f"Agent '{self.name}': Error closing exit_stack: {close_exc}", exc_info=True)
            else:
                print(f"Agent '{self.name}': No exit_stack was acquired, skipping close.")

            print(f"Agent '{self.name}': Exiting custom _run_async_impl.")
