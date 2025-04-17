from fastapi import APIRouter, HTTPException
from agent.langgraph.sampleagent.graphagent import ainvoke_graphagent
from agent.adk.sampleagent.adkagent import run_async_adkagent
from app.schemas.standardAiAgent import AtandardAiAgentRequest
from datetime import datetime

router = APIRouter()


@router.post("/aiagent/graph",
             summary="LangGraphのAIエージェントを実行します",
             description="LangGraphのAIエージェントを実行します")
async def aiagent_graph(request: AtandardAiAgentRequest):
    try:
        _input = f"""
        # メタ情報:
        - 現在の時刻は「{datetime.now()}」です。

        # 指示書
        {request.user_input}
        """
        result = await ainvoke_graphagent(_input)
        _response = {"result": result}
        # return AtandardAiAgentResponse(**_response)
        return _response
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred in the agent.")


@router.post("/aiagent/adk",
             summary="ADKのAIエージェントを実行します",
             description="ADKのAIエージェントを実行します")
async def aiagent_adk(request: AtandardAiAgentRequest):
    try:
        _input = f"""
        # メタ情報:
        - 現在の時刻は「{datetime.now()}」です。

        # 指示書
        {request.user_input}
        """
        result = await run_async_adkagent(_input)
        _response = {"result": result}
        # return AtandardAiAgentResponse(**_response)
        return _response
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        raise HTTPException(status_code=500, detail="An internal server error occurred in the agent.")
