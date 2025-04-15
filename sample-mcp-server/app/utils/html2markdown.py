import html2text
from bs4 import BeautifulSoup
import requests


def getMarkdown(url):
    try:
        result = {
            "state": "failed",
            "result": ""
        }
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            html_content = response.text
            # 関数を使ってHTMLをMarkdownに変換
            markdown_content = html_to_markdown(html_content)
            result["state"] = "success"
            result["result"] = markdown_content
            return result
        else:
            return str(response.status_code) + "エラー"
    except Exception as e:
        print(e)
        result["result"] = e
        return result


def html_to_markdown(html_content):
    # BeautifulSoupでHTMLをパース
    soup = BeautifulSoup(html_content, 'html.parser')

    # 不要な要素を削除（例: スクリプト、スタイル、ナビゲーションなど）
    for element in soup(['script', 'style', 'header', 'footer', 'nav', 'aside']):
        element.decompose()

    # html2textを設定してコードブロックに対応
    converter = html2text.HTML2Text()
    converter.body_width = 0
    converter.ignore_links = False
    converter.ignore_images = True
    converter.bypass_tables = False
    converter.single_line_break = True
    converter.code_style = True  # コードブロックを適切に処理

    # HTMLをMarkdownに変換
    markdown = converter.handle(str(soup))

    return markdown
