"""
Phase 6 settings 拡張スクリプト
"""

from pathlib import Path

settings_file = Path("src/video_asset_manualize/settings.py")

# 現在の内容を読み込む
content = settings_file.read_text(encoding='utf-8')

# LLM 設定を追加
if "LLM_PROVIDER_TYPE" not in content:
    llm_settings = """

# ===== LLM Settings (Phase 6) =====
LLM_PROVIDER_TYPE: str = "dummy"  # "dummy" or "openai"
LLM_MODEL: str = "gpt-3.5-turbo"  # OpenAI model name
OPENAI_API_KEY: str = ""  # Set via environment variable OPENAI_API_KEY
ENABLE_LLM_EXTRACTION: bool = False  # Enable LLM-based extraction in CLI
"""
    content += llm_settings
    settings_file.write_text(content, encoding='utf-8')
    print("✓ Updated: src/video_asset_manualize/settings.py (LLM settings added)")
else:
    print("⚠ LLM settings already present")

print("\n✅ settings.py の LLM 設定が更新されました")
