"""
Phase 6 実装自動生成スクリプト
LLM プロバイダーと関連モジュール
"""

from pathlib import Path

# ========== 1. llm_provider.py ==========
llm_provider = r'''"""
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
'''

# ========== 2. openai_llm_provider.py ==========
openai_llm_provider = r'''"""
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
'''

# ========== 3. prompt_templates.py ==========
prompt_templates = r'''"""
Prompt Templates - LLM プロンプトテンプレート
"""


class PromptTemplates:
    """LLM プロンプトテンプレート集"""
    
    @staticmethod
    def summary_prompt(transcript: str) -> str:
        """Summary 生成用プロンプト"""
        return f"""以下は動画の文字起こしです。

{transcript}

このコンテンツの要約を作成してください。以下の形式で答えてください：
- 目的: このコンテンツの主な目的
- 成果物: 完了時の期待結果
- 対象者: 想定される対象ユーザー

簡潔に、日本語で答えてください。"""
    
    @staticmethod
    def instruction_prompt(transcript: str, ocr_text: str = "") -> str:
        """Step/Procedure 抽出用プロンプト"""
        ocr_context = f"OCR テキスト:\n{ocr_text}\n\n" if ocr_text else ""
        
        return f"""以下は動画の文字起こしです。

{transcript}

{ocr_context}このコンテンツから、以下の操作手順を抽出してください。

JSON 形式で以下の構造で答えてください：
{{
  "chapters": [
    {{
      "title": "章タイトル",
      "procedures": [
        {{
          "title": "手順タイトル",
          "steps": [
            {{
              "order": 1,
              "action": "実施する操作",
              "expected_result": "期待される結果"
            }}
          ]
        }}
      ]
    }}
  ]
}}

各ステップは実行可能で、確認可能な粒度にしてください。"""
    
    @staticmethod
    def caution_prompt(transcript: str) -> str:
        """Caution/注意点 抽出用プロンプト"""
        return f"""以下は動画の文字起こしです。

{transcript}

このコンテンツで重要な注意点や警告、よくある間違いを抽出してください。

JSON 形式で以下の構造で答えてください：
{{
  "cautions": [
    "注意点1",
    "注意点2"
  ],
  "common_mistakes": [
    {{
      "mistake": "よくある間違い",
      "cause": "原因",
      "impact": "影響",
      "solution": "対策"
    }}
  ]
}}"""
    
    @staticmethod
    def faq_prompt(transcript: str, instructional_core: str) -> str:
        """FAQ 候補生成用プロンプト"""
        return f"""以下は動画の文字起こしと抽出された手順です。

文字起こし:
{transcript}

抽出された手順:
{instructional_core}

これらのコンテンツをもとに、よくある質問と回答を生成してください。

JSON 形式で以下の構造で答えてください：
{{
  "faqs": [
    {{
      "question": "質問内容",
      "answer": "回答内容",
      "priority": "high"
    }}
  ]
}}

3-5 個のよくある質問を生成してください。"""
'''

# ファイルを作成
src_dir = Path("src/video_asset_manualize")

files = {
    "llm_provider.py": llm_provider,
    "openai_llm_provider.py": openai_llm_provider,
    "prompt_templates.py": prompt_templates,
}

for filename, content in files.items():
    file_path = src_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Created: {file_path}")

print("\n✅ Phase 6 基盤モジュール作成完了")
