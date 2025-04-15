# ADK-MCP Integration Sample

このリポジトリは、[Agent Development Kit](https://google.github.io/adk-docs/)(ADK)と[MCP](https://modelcontextprotocol.io/introduction)サーバーを連携させたサンプルアプリケーションです。  
自然言語で入力されたリクエストをMCPサーバーに送信し、AIエージェントがタスクを処理する流れを構築しています。

## 🚀 概要

- ADK を通じて、ユーザーの自然言語リクエストを受け取ります
- リクエストは MCP サーバーにルーティングされ、対応するエージェントへディスパッチされます
- 結果をユーザーに自然言語でフィードバックします

## 🛠 使用技術

- Python 3.12+
- Google Agent Development Kit

## 📦 セットアップ

### 1. リポジトリをクローン

```bash
git clone https://github.com/Kewton/adk-mcp-starter.git
cd mcp-gadk-sample
```

### 2. mcp-serverのセットアップ
```bash
cd sample-mcp-server
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
### 3. ADK-Agentのセットアップ
```bash
cd sample-adk-agent
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```
### 4. 実行
- MCPサーバーの起動
```bash
cd sample-mcp-server
python main.py
```
- ADK Web Serverの起動<br>
ADK CLIを使用します
```bash
cd sample-adk-agent
adk web
```
#### 動作確認1
1. ADK Web Serverを起動すると「For local testing, access at http://・・・」が表示されます<br>
表示されたURLをクリックするとWEB GUIが起動されます
1. 左上のドロップダウンリストにてAIエージェントを選択します。ここでは"sampleagent"を選択します
1. 右下の入力欄からAIエージェントに指示を出すと結果が出力されます

#### 動作確認2
ADK Wev Serverを使用せず、直接AIエージェントを実行します
```bash
cd sample-adk-agent
python adkagent.py
```