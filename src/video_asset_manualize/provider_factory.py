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

    @staticmethod
    def create_llm_provider(provider_type='dummy', **kwargs):
        """LLM プロバイダーを作成"""
        if provider_type == 'openai':
            try:
                from .openai_llm_provider import OpenAILLMProvider
                api_key = kwargs.get('api_key') or os.getenv('OPENAI_API_KEY')
                model = kwargs.get('model', 'gpt-3.5-turbo')
                if not api_key:
                    raise ValueError("OPENAI_API_KEY is required for OpenAI provider")
                return OpenAILLMProvider(api_key=api_key, model=model)
            except ImportError:
                raise ImportError("OpenAI library not found. Install with: pip install openai")
        else:
            from .llm_provider import DummyLLMProvider
            return DummyLLMProvider()

