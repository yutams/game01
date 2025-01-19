from bs4 import BeautifulSoup
from jinja2 import Template

# ファイルパス
input_file = "index.html"  # 入力元
output_file = input_file  # 出力先
template_file = "index_template.html"  # テンプレート

# HTMLファイルを読み込む
with open(input_file, "r", encoding="utf-8") as file:
    html_content = file.read()

# BeautifulSoupを使ってHTMLを解析
soup = BeautifulSoup(html_content, "html.parser")

# スクリプトタグを検索
script_tag = soup.find("script", string=lambda text: text and "launchPyxel" in text)

# `launchPyxel` の行から値を抽出
if script_tag:
    script_content = script_tag.string
    # `name` と `base64` の値を取得
    import re

    name_match = re.search(r'name:\s*"([^"]+)"', script_content)
    base64_match = re.search(r'base64:\s*"([^"]+)"', script_content)

    name_value = name_match.group(1) if name_match else None
    base64_value = base64_match.group(1) if base64_match else None
else:
    print("launchPyxelが見つかりませんでした")

# テンプレートを読み込む
with open(template_file, "r", encoding="utf-8") as file:
    html_template = file.read()

# 値を埋め込む
template = Template(html_template)
output_html = template.render(name=name_value, base64=base64_value)

# 更新されたHTMLを保存
with open(output_file, "w", encoding="utf-8") as file:
    file.write(output_html)

print(f"テンプレートを反映")
