# ADK-MCP Integration Sample

- このリポジトリは、[Agent Development Kit](https://google.github.io/adk-docs/)(ADK)と[MCP](https://modelcontextprotocol.io/introduction)サーバーを連携させたサンプルアプリケーションです。
- また、[LangGraph](https://github.com/langchain-ai/langchain-mcp-adapters)とMCPサーバーを連携させたサンプルアプリケーションも用意しています。
- 自然言語で入力されたリクエストをMCPサーバーに送信し、AIエージェントがタスクを処理する流れを構築しています。

## 🚀 概要

- ADK-MCP
    - ADK を通じて、ユーザーの自然言語リクエストを受け取ります
    - リクエストは MCP サーバーにルーティングされ、対応するエージェントへディスパッチされます
    - 結果をユーザーに自然言語でフィードバックします
- LangGraph-MCP
    - LangGraph を通じて、ユーザーの自然言語リクエストを受け取ります
    - リクエストは MCP サーバーにルーティングされ、対応するエージェントへディスパッチされます
    - 結果をユーザーに自然言語でフィードバックします
- FastAPI-(ADK/LangGraph)-MCP
    - RestAPI を通じて、ユーザーの自然言語リクエストを受け取ります
    - リクエストは ADKもしくはLangGraphで構築したエージェントに渡されたあと、 MCP サーバーにルーティングされ、対応するエージェントへディスパッチされます
    - 結果をユーザーに自然言語でフィードバックします

## 🛠 使用技術

- Python 3.12+
- Google Agent Development Kit
- MCP
- LangGraph

## 📦 セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/Kewton/adk-mcp-starter.git
cd mcp-gadk-sample
```

---

### 2. セットアップ
#### (1) mcp-serverのセットアップ
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-mcp-server
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

#### (2) ADK-Agentのセットアップ
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-adk-agent
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

#### (3) LangGraph-Agentのセットアップ
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-langGraph-agent
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

#### (4) ADK-AgentとLangGraph-AgentをラッピングするFastAPIのセットアップ
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-fast-api
python3 -m venv venv
source venv/bin/activate

pip install --upgrade pip
pip install -r requirements.txt
```

---

### 3. ADK-Agentの実行と動作確認（ADK Web Server 経由）

#### (1) `.env` ファイルの作成

**sample-mcp-server/.env**
```env
HOST=127.0.0.1
PORT=8001
```

**sample-adk-agent/.env**
```env
SSE_SERVER_PARAMS_URL=http://localhost:8001/sse
MODEL=gemini-2.0-flash
GOOGLE_API_KEY=<your api key>
```

#### (2) MCP サーバーの起動
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-mcp-server
source venv/bin/activate

python main.py
```

#### (3) ADK Web Server の起動
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-adk-agent
source venv/bin/activate

adk web
```

起動後、「For local testing, access at http://...」と表示される URL にアクセスすると、ADK Web Server の GUI が起動します。

#### (4) AI エージェントに指示を送信

- 画面左上のドロップダウンから `"sampleagent"` を選択
- 右下の入力フィールドから自然言語で指示を送信 → MCP サーバー経由で実行され、結果が表示されます

![スクリーンショット](https://qiita-image-store.s3.ap-northeast-1.amazonaws.com/0/35883/111283be-c3bc-485b-9900-57ed76be01df.png)


### 4. ADK-Agentの実行と動作確認（直接実行）
[3. ADK-Agentの実行と動作確認（ADK Web Server 経由）](#3-adk-agentの実行と動作確認adk-web-server-経由)の(1)~(2)は共通です。


#### (3) ADK-Agent の起動
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-adk-agent
source venv/bin/activate

python adkagent.py
```

### 5. MCPサーバーを利用したLangGraphの実行と動作確認
#### (1) `.env` ファイルの作成

**sample-mcp-server/.env**
```env
HOST=127.0.0.1
PORT=8001
```

**sample-langGraph-agent/.env**
```env
SSE_SERVER_PARAMS_URL=http://localhost:8001/sse
OPENAI_API_KEY=<your api key>
```

#### (2) MCP サーバーの起動
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-mcp-server
source venv/bin/activate

python main.py
```

#### (3) LangGraph-Agent の起動
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-langGraph-agent
source venv/bin/activate

python graph.py
```

### 6. ADK-AgentとLangGraph-AgentをラッピングするFastAPIの実行

#### (1) `.env` ファイルの作成

**sample-mcp-server/.env**
```env
HOST=127.0.0.1
PORT=8001
```

**sample-langGraph-agent/.env**
```env
OPENAI_API_KEY=<your api key>
GOOGLE_API_KEY=<your api key>
LOG_DIR=./log
LOG_LEVEL=INFO
SSE_SERVER_PARAMS_URL=http://localhost:8001/sse
ADK_AGENT_MODEL=gemini-2.0-flash
GRAPH_AGENT_MODEL=gpt-4o-mini
```

#### (2) MCP サーバーの起動
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-mcp-server
source venv/bin/activate

python main.py
```

#### (3) FastAPI の起動
ターミナルを起動して下記コマンドを実行します。
```bash
cd sample-langGraph-agent
source venv/bin/activate

uvicorn app.main:app --reload
```

#### (4) 動作確認
ターミナルを起動して下記コマンドを実行します。
```bash
# langGraph-Agentの実行
curl -X POST "http://127.0.0.1:8000/aiagent-api/v1/aiagent/graph" \
    -H "Content-Type: application/json" \
    -d '{
      "user_input": "https://github.com/Kewton/adk-mcp-starter の記事をマークダウン形式に変換して出力してください"
    }'

# ADK-Agentの実行
curl -X POST "http://127.0.0.1:8000/aiagent-api/v1/aiagent/adk" \
    -H "Content-Type: application/json" \
    -d '{
      "user_input": "https://github.com/Kewton/adk-mcp-starter の記事をマークダウン形式に変換して出力してください"
    }'
```