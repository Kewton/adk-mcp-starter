from pydantic import BaseModel
from typing import List, Dict, Any # List, Dict, Any をインポート


class AtandardAiAgentRequest(BaseModel):
    user_input: str
    model_name: str | None = None
    max_iterations: int | None = None
    thought_process_Flg: bool = True


# # チャットメッセージの形式を表すモデル
# class ChatMessage(BaseModel):
#     role: str
#     content: str
#     # 必要であれば他のフィールド (例: name: Optional[str] = None)


# class AtandardAiAgentResponse(BaseModel):
#     # result フィールドを ChatMessage モデルのリストとして定義
#     result: List[ChatMessage]
