"""
provider_factory.py と settings.py を拡張
OCR provider 切替機構を追加
"""

from pathlib import Path

# ========== 1. provider_factory.py を拡張 ==========
factory_file = Path("src/video_asset_manualize/provider_factory.py")

with open(factory_file, "r", encoding="utf-8") as f:
    factory_content = f.read()

# create_ocr_provider メソッドを修正
new_create_ocr = '''    @staticmethod
    def create_ocr_provider(
        provider_type: Literal["dummy", "easyocr"] = "dummy",
        **kwargs
    ) -> OCRProvider:
        """
        OCR Provider を生成
        
        Args:
            provider_type: "dummy" または "easyocr"
            **kwargs: Provider に渡すオプション
        
        Returns:
            OCRProvider インスタンス
        """
        if provider_type == "easyocr":
            try:
                from .easyocr_provider import EasyOCRProvider
                return EasyOCRProvider(
                    languages=kwargs.get("languages", ["ja", "en"]),
                    gpu=kwargs.get("gpu", False)
                )
            except ImportError:
                raise ImportError(
                    "EasyOCR provider requires easyocr. "
                    "Install with: pip install easyocr"
                )
        else:
            return DummyOCRProvider()'''

# 古い create_ocr_provider を新しいバージョンで置き換え
import re
factory_content = re.sub(
    r'@staticmethod\s+def create_ocr_provider\([\s\S]*?return DummyOCRProvider\(\)',
    new_create_ocr,
    factory_content
)

with open(factory_file, "w", encoding="utf-8") as f:
    f.write(factory_content)

print("✓ provider_factory.py を拡張しました")

# ========== 2. settings.py を拡張 ==========
settings_file = Path("src/video_asset_manualize/settings.py")

with open(settings_file, "r", encoding="utf-8") as f:
    settings_content = f.read()

# OCR_PROVIDER_TYPE の後に詳細設定を追加
ocr_settings = '''    OCR_PROVIDER_TYPE: str = "dummy"  # "dummy" or "easyocr"
    EASYOCR_LANGUAGES: list = ["ja", "en"]  # OCR対象言語
    EASYOCR_GPU: bool = False  # GPU を使用するか
'''

# 既存の OCR_PROVIDER_TYPE を置き換え
settings_content = re.sub(
    r'OCR_PROVIDER_TYPE: str = "dummy"  # "dummy" or future "easyocr"',
    ocr_settings,
    settings_content
)

with open(settings_file, "w", encoding="utf-8") as f:
    f.write(settings_content)

print("✓ settings.py を拡張しました")

print("\n✅ Provider Factory と Settings を拡張完了")
