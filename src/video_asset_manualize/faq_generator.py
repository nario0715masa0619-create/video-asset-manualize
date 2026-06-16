"""
FAQ Generator - LLM を使った FAQ 生成
"""

import json
from typing import List, Dict, Any
from .llm_provider import LLMProvider
from .prompt_templates import PromptTemplates


class FAQGenerator:
    """LLM を使った FAQ 候補生成"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize generator
        
        Args:
            llm_provider: LLM プロバイダー
        """
        self.llm = llm_provider
    
    def generate_faqs(
        self,
        evidence_text: str,
        instructional_core: str
    ) -> List[Dict[str, str]]:
        """
        FAQ 候補を生成
        
        Args:
            evidence_text: 抽出ログ（文字起こしやOCR等）
            instructional_core: 抽出された手順
        
        Returns:
            FAQ リスト
        """
        try:
            prompt = PromptTemplates.faq_prompt(evidence_text, instructional_core)
            response = self.llm.generate_text(prompt, max_tokens=1000)
            
            # JSON をパース
            faqs = self._parse_json_response(response)
            return faqs
        
        except Exception as e:
            return self._default_faqs()
    
    def _parse_json_response(self, response: str) -> List[Dict[str, str]]:
        """JSON 応答をパース"""
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                return data.get("faqs", [])
        except:
            pass
        
        return self._default_faqs()
    
    def _default_faqs(self) -> List[Dict[str, str]]:
        """デフォルト FAQ"""
        return [
            {
                "question": "このコンテンツは何ですか？",
                "answer": "動画から自動抽出されたコンテンツです。",
                "priority": "high"
            }
        ]
