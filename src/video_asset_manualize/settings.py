"""
Configuration and settings management for VideoAsset Manualize.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """
    
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

    # Provider settings
    TRANSCRIPT_PROVIDER_TYPE: str = "dummy"  # "dummy" or "whisper"
    WHISPER_MODEL: str = "base"  # tiny, base, small, medium, large
    WHISPER_LANGUAGE: str = "ja"  # Language code
    OCR_PROVIDER_TYPE: str = "dummy"  # "dummy" or future "easyocr"


    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
