"""
Phase 6 build_training_asset_pipeline 修正スクリプト
"""

from pathlib import Path

pipeline_file = Path("src/video_asset_manualize/build_training_asset_pipeline.py")
content = pipeline_file.read_text(encoding='utf-8')

# output_dir を Path に変換
old_line = "output_dir = output_dir or settings.EXPORTS_DIR"
new_lines = """output_dir = Path(output_dir or settings.EXPORTS_DIR)
        output_dir.mkdir(parents=True, exist_ok=True)"""

content = content.replace(old_line, new_lines)

pipeline_file.write_text(content, encoding='utf-8')
print("✓ Updated: src/video_asset_manualize/build_training_asset_pipeline.py")
print("\n✅ build_training_asset_pipeline.py が修正されました")
