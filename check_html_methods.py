"""
html_manual_renderer.py からメソッド情報を抽出
"""

from pathlib import Path
import re

html_renderer_file = Path("src/video_asset_manualize/html_manual_renderer.py")

if html_renderer_file.exists():
    content = html_renderer_file.read_text(encoding='utf-8')
    
    # render メソッドを探す
    match = re.search(r'def render\(self[^)]*\):[^}]+?(?=\n    def |\nclass |\Z)', content, re.DOTALL)
    if match:
        method_code = match.group(0)
        # 最初の10行を表示
        lines = method_code.split('\n')[:15]
        print("render method preview:")
        for line in lines:
            print(line)
    
    # 戻り値の型をチェック
    methods = re.findall(r'def (\w+)\(', content)
    print("\nAvailable methods in HTMLManualRenderer:")
    for method in methods:
        print(f"  - {method}")
else:
    print("html_manual_renderer.py not found")
