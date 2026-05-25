"""
provider_factory.py を完全に再生成
"""

from pathlib import Path

factory_file = Path("src/video_asset_manualize/provider_factory.py")

new_factory = r'''"""
Provider Factory - Provider の生成と切り替え
"""

from typing import Literal
from .transcript_provider import (
    TranscriptProvider,
    DummyTranscriptProvider
)
from .ocr_provider import OCRProvider, DummyOCRProvider


class ProviderFactory:
    """Provider ファクトリ"""
    
    @staticmethod
    def create_transcript_provider(
        provider_type: Literal["dummy", "whisper"] = "dummy",
        **kwargs
    ) -> TranscriptProvider:
        """
        Transcript Provider を生成
        
        Args:
            provider_type: "dummy" または "whisper"
            **kwargs: Provider に渡すオプション
        
        Returns:
            TranscriptProvider インスタンス
        """
        if provider_type == "whisper":
            try:
                from .whisper_transcript_provider import WhisperTranscriptProvider
                return WhisperTranscriptProvider(
                    model=kwargs.get("model", "base"),
                    language=kwargs.get("language", "ja")
                )
            except ImportError:
                raise ImportError(
                    "Whisper provider requires openai-whisper. "
                    "Install with: pip install openai-whisper"
                )
        else:
            return DummyTranscriptProvider()
    
    @staticmethod
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
            return DummyOCRProvider()
'''

with open(factory_file, "w", encoding="utf-8") as f:
    f.write(new_factory)

print("✓ provider_factory.py を完全に再生成しました")
