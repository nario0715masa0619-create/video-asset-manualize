"""
settings.py を完全に再生成
"""

from pathlib import Path

settings_file = Path("src/video_asset_manualize/settings.py")

new_settings = r'''"""
Configuration and settings management for VideoAsset Manualize.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    SRC_DIR: Path = PROJECT_ROOT / "src"
    SAMPLES_DIR: Path = PROJECT_ROOT / "samples"
    SCHEMAS_DIR: Path = PROJECT_ROOT / "schemas"
    OUTPUT_DIR: Path = PROJECT_ROOT / "output"
    EXPORTS_DIR: Path = OUTPUT_DIR / "exports"
    SCHEMA_VERSION: str = "0.1.0"
    TRAINING_ASSET_SCHEMA_FILE: Path = SCHEMAS_DIR / "training_asset_spec.schema.json"
    TEMPLATES_DIR: Path = SRC_DIR / "video_asset_manualize" / "templates"
    HTML_TEMPLATE_FILE: Path = TEMPLATES_DIR / "manual_template.html"
    LOG_LEVEL: str = "INFO"
    ENABLE_SCHEMA_VALIDATION: bool = True
    ENABLE_HTML_GENERATION: bool = True
    ENABLE_PDF_GENERATION: bool = True
    PDF_PAPER_SIZE: str = "A4"
    PDF_MARGIN_TOP: int = 20
    PDF_MARGIN_BOTTOM: int = 20
    PDF_MARGIN_LEFT: int = 20
    PDF_MARGIN_RIGHT: int = 20
    
    # Provider settings (Phase 4)
    TRANSCRIPT_PROVIDER_TYPE: str = "dummy"
    WHISPER_MODEL: str = "base"
    WHISPER_LANGUAGE: str = "ja"
    
    # OCR Provider settings (Phase 5)
    OCR_PROVIDER_TYPE: str = "dummy"
    EASYOCR_LANGUAGES: list = ["ja", "en"]
    EASYOCR_GPU: bool = False
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)

settings = Settings()
'''

with open(settings_file, "w", encoding="utf-8") as f:
    f.write(new_settings)

print("✓ settings.py を完全に再生成しました")
