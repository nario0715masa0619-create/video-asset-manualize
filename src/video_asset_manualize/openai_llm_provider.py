"""
OpenAI LLM Provider - OpenAI API を使った LLM 実装
"""

from typing import Optional
from .llm_provider import LLMProvider


class OpenAILLMProvider(LLMProvider):
    """OpenAI API を使った LLM プロバイダー"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-3.5-turbo"):
        """
        Initialize OpenAI LLM provider
        
        Args:
            api_key: OpenAI API キー
            model: 使用するモデル
        """
        self.api_key = api_key
        self.model = model
        self.client = None
        self._initialize_client()
    
    def _initialize_client(self):
        """OpenAI クライアントを初期化"""
        try:
            from openai import OpenAI
            
            if not self.api_key:
                raise ValueError(
                    "OpenAI API key not found. "
                    "Set OPENAI_API_KEY environment variable or pass api_key parameter."
                )
            
            self.client = OpenAI(api_key=self.api_key)
        
        except ImportError:
            raise ImportError(
                "OpenAI provider requires openai library. "
                "Install with: pip install openai"
            )
        except Exception as e:
            raise RuntimeError(f"OpenAI initialization failed: {str(e)}")
    
    def generate_text(self, prompt: str, max_tokens: int = 1000) -> str:
        """
        OpenAI API でテキストを生成
        
        Args:
            prompt: プロンプト
            max_tokens: 最大トークン数
        
        Returns:
            生成されたテキスト
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a helpful assistant."},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=max_tokens,
                temperature=0.7
            )
            
            return response.choices[0].message.content.strip()
        
        except Exception as e:
            raise RuntimeError(f"OpenAI API call failed: {str(e)}")
