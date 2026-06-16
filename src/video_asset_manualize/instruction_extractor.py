"""
Instruction Extractor - LLM を使った step/procedure 抽出
"""

import json
from typing import List, Dict, Any
from .llm_provider import LLMProvider
from .prompt_templates import PromptTemplates


class InstructionExtractor:
    """LLM を使った instruction 抽出"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize extractor
        
        Args:
            llm_provider: LLM プロバイダー
        """
        self.llm = llm_provider
    
    def extract_instructions(
        self,
        evidence_text: str
    ) -> Dict[str, Any]:
        """
        Transcript から chapters を抽出
        
        Args:
            evidence_text: 抽出ログ（文字起こしやOCR等）
        
        Returns:
            chapters 構造
        """
        try:
            prompt = PromptTemplates.instruction_prompt(evidence_text)
            response = self.llm.generate_text(prompt, max_tokens=2000)
            
            # JSON をパース
            result = self._parse_json_response(response)
            return result
        
        except Exception as e:
            return self._default_instructions()
    
    def _parse_json_response(self, response: str) -> Dict[str, Any]:
        """JSON 応答をパース"""
        try:
            # JSON ブロックを抽出
            import re
            json_match = re.search(r'\{.*\}', response, re.DOTALL)
            if json_match:
                json_str = json_match.group()
                data = json.loads(json_str)
                return data
        except:
            pass
        
        return self._default_instructions()
    
    def _default_instructions(self) -> Dict[str, Any]:
        """デフォルト instructions"""
        return {
            "chapters": [
                {
                    "chapter_id": "chapter-001",
                    "title": "自動抽出された手順",
                    "procedures": [
                        {
                            "procedure_id": "procedure-001",
                            "title": "基本操作",
                            "steps": [
                                {
                                    "step_id": "step-001",
                                    "order": 1,
                                    "action": "LLM で自動抽出された操作です",
                                    "expected_result": "完了します"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
