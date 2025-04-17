# mcp-server用の環境構築
```
cd sample-fast-api
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```

# 実行
```
uvicorn app.main:app --reload
```

# test
```
curl -X POST "http://127.0.0.1:8000/aiagent-api/v1/aiagent/graph" \
    -H "Content-Type: application/json" \
    -d '{
      "user_input": "https://github.com/Kewton/adk-mcp-starter の記事をマークダウン形式に変換して出力してください"
    }'

curl -X POST "http://127.0.0.1:8000/aiagent-api/v1/aiagent/adk" \
    -H "Content-Type: application/json" \
    -d '{
      "user_input": "https://github.com/Kewton/adk-mcp-starter の記事をマークダウン形式に変換して出力してください"
    }'
```