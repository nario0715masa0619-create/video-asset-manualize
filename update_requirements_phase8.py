"""
Phase 8 requirements.txt 更新スクリプト
"""

from pathlib import Path

requirements_file = Path("requirements.txt")

# 既存の内容を読み込む
if requirements_file.exists():
    current = requirements_file.read_text(encoding='utf-8').strip()
else:
    current = ""

# Streamlit 関連の依存を追加
streamlit_deps = """
# Web UI (Phase 8)
streamlit>=1.28.0
"""

# 重複を避けるため、Streamlit が既にあるかチェック
if "streamlit" not in current:
    new_content = current + "\n" + streamlit_deps.strip() + "\n"
    requirements_file.write_text(new_content, encoding='utf-8')
    print("OK: requirements.txt updated with streamlit")
else:
    print("OK: streamlit already in requirements.txt")

# 内容を表示
print("\n=== requirements.txt ===")
print(requirements_file.read_text(encoding='utf-8'))
