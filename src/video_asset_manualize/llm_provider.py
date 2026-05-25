"""
LLM Provider - 言語モデル抽象インターフェース
"""

from abc import ABC, abstractmethod
from typing import Dict, Any


class LLMProvider(ABC):
    """LLM プロバイダーの抽象基底クラス"""
    
    @abstractmethod
    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        テキストを生成
        
        Args:
            prompt: プロンプト
            max_tokens: 最大トークン数
        
        Returns:
            生成されたテキスト
        """
        pass


class DummyLLMProvider(LLMProvider):
    """ダミー実装 - テスト用"""
    
    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """ダミーテキストを返す"""
        return "これはダミー LLM の出力です。実装の確認用です。"
