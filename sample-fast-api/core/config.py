from pydantic_settings import BaseSettings  # pydantic_settingsからインポート
from pydantic import Field
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    OPENAI_API_KEY: str = Field(default="OPENAI_API_KEY", env="OPENAI_API_KEY")
    GOOGLE_API_KEY: str = Field(default="GOOGLE_API_KEY", env="GOOGLE_API_KEY")
    LOG_DIR: str = Field(default="./", env="LOG_DIR")
    LOG_LEVEL: str = Field(default="INFO", env="LOG_LEVEL")
    SSE_SERVER_PARAMS_URL: str = Field(default="SSE_SERVER_PARAMS_URL", env="SSE_SERVER_PARAMS_URL")
    ADK_AGENT_MODEL: str = Field(default="ADK_AGENT_MODEL", env="ADK_AGENT_MODEL")
    GRAPH_AGENT_MODEL: str = Field(default="GRAPH_AGENT_MODEL", env="GRAPH_AGENT_MODEL")

# インスタンス生成
settings = Settings()
