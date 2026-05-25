"""
pdf_manual_renderer.py からメソッド名を抽出
"""

from pathlib import Path
import re

pdf_renderer_file = Path("src/video_asset_manualize/pdf_manual_renderer.py")

if pdf_renderer_file.exists():
    content = pdf_renderer_file.read_text(encoding='utf-8')
    
    # def で始まるメソッドを探す
    methods = re.findall(r'def (\w+)\(', content)
    print("Available methods in PDFManualRenderer:")
    for method in methods:
        print(f"  - {method}")
else:
    print("pdf_manual_renderer.py not found")
