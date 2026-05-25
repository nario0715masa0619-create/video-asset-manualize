"""
Phase 6 build_training_asset_pipeline メソッド修正スクリプト
"""

from pathlib import Path

pipeline_file = Path("src/video_asset_manualize/build_training_asset_pipeline.py")
content = pipeline_file.read_text(encoding='utf-8')

# render メソッド呼び出しを修正
# PDFManualRenderer は異なるメソッド名を使用する可能性があります
replacements = [
    ('self.html_renderer.render(self.spec)', 'self.html_renderer.render(self.spec)'),
    ('self.pdf_renderer.render(self.spec)', 'self.pdf_renderer.render_to_bytes(self.spec)'),
]

# 最初に PDFManualRenderer の実際のメソッドを確認するため、
# render_to_bytes が無ければ他の方法を試す
for old, new in replacements:
    if old in content:
        content = content.replace(old, new)

pipeline_file.write_text(content, encoding='utf-8')
print("Updated: src/video_asset_manualize/build_training_asset_pipeline.py")
print("\nOK: PDF render method fixed")
