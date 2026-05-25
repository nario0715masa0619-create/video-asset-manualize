"""
settings.py を拡張して Provider 設定を追加
"""

from pathlib import Path

settings_file = Path("src/video_asset_manualize/settings.py")

# 現在のコンテンツを読み込み
with open(settings_file, "r", encoding="utf-8") as f:
    content = f.read()

# PDF_MARGIN_RIGHT = 20 の直後に Provider 設定を追加
provider_settings = '''
    # Provider settings
    TRANSCRIPT_PROVIDER_TYPE: str = "dummy"  # "dummy" or "whisper"
    WHISPER_MODEL: str = "base"  # tiny, base, small, medium, large
    WHISPER_LANGUAGE: str = "ja"  # Language code
    OCR_PROVIDER_TYPE: str = "dummy"  # "dummy" or future "easyocr"
'''

# 挿入位置を探す
insert_marker = "PDF_MARGIN_RIGHT: int = 20"
if insert_marker in content:
    insert_pos = content.find(insert_marker) + len(insert_marker)
    new_content = (
        content[:insert_pos] + "\n" + provider_settings + "\n" + content[insert_pos:]
    )
else:
    new_content = content

# ファイルに保存
with open(settings_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✓ settings.py に Provider 設定を追加しました")
