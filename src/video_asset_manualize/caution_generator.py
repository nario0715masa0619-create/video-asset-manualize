"""
Caution Generator - LLM を使った注意点生成
"""

import json
from typing import List, Dict, Any
from .llm_provider import LLMProvider
from .prompt_templates import PromptTemplates


class CautionGenerator:
    """LLM を使った caution/注意点生成"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize generator
        
        Args:
            llm_provider: LLM プロバイダー
        """
        self.llm = llm_provider
    
    def generate_cautions(self, transcript: str) -> Dict[str, Any]:
        """
        Transcript から cautions を生成
        
        Args:
            transcript: 文字起こし
        
        Returns:
            cautions と common_mistakes
        """
        try:
            prompt = PromptTemplates.caution_prompt(transcript)
            response = self.llm.generate_text(prompt, max_tokens=1000)
            
            # JSON をパース
            result = self._parse_json_response(response)
            return result
        
        except Exception as e:
            return self._default_cautions()
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """JSON 応答をパース"""
        try:
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                return data
        except:
            pass
        
        return self._default_cautions()
    
    def _default_cautions(self) -> Dict[str, Any]:
        """デフォルト cautions"""
        return {
            "global_cautions": [
                "このコンテンツは自動抽出です"
            ],
            "common_mistakes": []
        }
