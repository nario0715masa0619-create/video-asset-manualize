"""
settings.py のインデントエラーを修正
"""

from pathlib import Path

settings_file = Path("src/video_asset_manualize/settings.py")

# ファイルを読み込み
with open(settings_file, "r", encoding="utf-8") as f:
    content = f.read()

# 問題のある部分を特定して修正
# OCR_PROVIDER_TYPE 周辺のインデントを修正
lines = content.split("\n")
fixed_lines = []
in_ocr_section = False

for i, line in enumerate(lines):
    # インデントが不正な行を修正
    if "OCR_PROVIDER_TYPE" in line and line.startswith("    OCR_PROVIDER_TYPE"):
        # 正しいインデント（4 スペース）で出力
        fixed_lines.append("    OCR_PROVIDER_TYPE: str = \"dummy\"  # \"dummy\" or \"easyocr\"")
    elif "EASYOCR_LANGUAGES" in line and line.startswith("    EASYOCR_LANGUAGES"):
        fixed_lines.append("    EASYOCR_LANGUAGES: list = [\"ja\", \"en\"]  # OCR対象言語")
    elif "EASYOCR_GPU" in line and line.startswith("    EASYOCR_GPU"):
        fixed_lines.append("    EASYOCR_GPU: bool = False  # GPU を使用するか")
    else:
        fixed_lines.append(line)

new_content = "\n".join(fixed_lines)

with open(settings_file, "w", encoding="utf-8") as f:
    f.write(new_content)

print("✓ settings.py のインデントを修正しました")
