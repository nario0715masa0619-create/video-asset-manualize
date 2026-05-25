"""
Summary Generator - LLM を使った summary 生成
"""

import json
from typing import Dict, Any
from .llm_provider import LLMProvider
from .prompt_templates import PromptTemplates


class SummaryGenerator:
    """LLM を使った summary 生成"""
    
    def __init__(self, llm_provider: LLMProvider):
        """
        Initialize generator
        
        Args:
            llm_provider: LLM プロバイダー
        """
        self.llm = llm_provider
    
    def generate_summary(self, transcript: str) -> Dict[str, str]:
        """
        Transcript から summary を生成
        
        Args:
            transcript: 文字起こし
        
        Returns:
            summary dict
        """
        try:
            prompt = PromptTemplates.summary_prompt(transcript)
            response = self.llm.generate_text(prompt, max_tokens=500)
            
            # 応答をパース
            summary = self._parse_summary_response(response)
            return summary
        
        except Exception as e:
            return self._default_summary(str(e))
    
    def _parse_summary_response(self, response: str) -> Dict[str, str]:
        """応答をパース"""
        try:
            lines = response.split("\n")
            summary = {
                "purpose_summary": "",
                "outcome_summary": "",
                "audience_summary": ""
            }
            
            current_key = None
            for line in lines:
                line = line.strip()
                if line.startswith("- 目的:"):
                    summary["purpose_summary"] = line.replace("- 目的:", "").strip()
                elif line.startswith("- 成果物:"):
                    summary["outcome_summary"] = line.replace("- 成果物:", "").strip()
                elif line.startswith("- 対象者:"):
                    summary["audience_summary"] = line.replace("- 対象者:", "").strip()
            
            return summary
        except:
            return self._default_summary("")
    
    def _default_summary(self, error: str = "") -> Dict[str, str]:
        """デフォルト summary"""
        return {
            "purpose_summary": "動画コンテンツの自動抽出です",
            "outcome_summary": "手順を完了できる状態を目指します",
            "audience_summary": "すべてのユーザー"
        }
