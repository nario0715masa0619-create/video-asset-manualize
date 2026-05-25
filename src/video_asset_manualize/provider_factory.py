"""
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
        return DummyOCRProvider()
