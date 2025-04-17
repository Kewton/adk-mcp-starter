from fastapi import FastAPI
from app.api.v1 import common_endpoints
from app.api.v1 import agent_endpoints


app = FastAPI(
    title="My API",
    description="APIドキュメント",
    version="1.0.0",
    root_path="/aiagent-api",
    swagger_ui_parameters={
        "docExpansion": "list",  # サイドバーにAPIリンクを表示
        "defaultModelsExpandDepth": -1  # モデルはサイドバーに表示しない
    }
)

app.include_router(common_endpoints.router, prefix="/v1")
app.include_router(agent_endpoints.router, prefix="/v1")
