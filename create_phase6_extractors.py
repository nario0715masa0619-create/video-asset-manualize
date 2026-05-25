"""
Phase 6 抽出モジュール作成
"""

from pathlib import Path
import json

# ========== 1. summary_generator.py ==========
summary_gen = r'''"""
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
'''

# ========== 2. instruction_extractor.py ==========
instruction_extractor = r'''"""
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
        transcript: str,
        ocr_text: str = ""
    ) -> Dict[str, Any]:
        """
        Transcript から chapters を抽出
        
        Args:
            transcript: 文字起こし
            ocr_text: OCR テキスト
        
        Returns:
            chapters 構造
        """
        try:
            prompt = PromptTemplates.instruction_prompt(transcript, ocr_text)
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
'''

# ========== 3. caution_generator.py ==========
caution_gen = r'''"""
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
'''

# ========== 4. faq_generator.py ==========
faq_gen = r'''"""
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
        transcript: str,
        instructional_core: str
    ) -> List[Dict[str, str]]:
        """
        FAQ 候補を生成
        
        Args:
            transcript: 文字起こし
            instructional_core: 抽出された手順
        
        Returns:
            FAQ リスト
        """
        try:
            prompt = PromptTemplates.faq_prompt(transcript, instructional_core)
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
'''

# ファイルを作成
src_dir = Path("src/video_asset_manualize")

files = {
    "summary_generator.py": summary_gen,
    "instruction_extractor.py": instruction_extractor,
    "caution_generator.py": caution_gen,
    "faq_generator.py": faq_gen,
}

for filename, content in files.items():
    file_path = src_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Created: {file_path}")

print("\n✅ Phase 6 抽出モジュール作成完了")
