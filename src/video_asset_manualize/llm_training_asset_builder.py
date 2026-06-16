"""
LLM Training Asset Builder - source_evidence から training_asset_spec を LLM で生成
"""

import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4
from typing import Dict, Any, Optional

from .llm_provider import LLMProvider, DummyLLMProvider
from .openai_llm_provider import OpenAILLMProvider
from .summary_generator import SummaryGenerator
from .instruction_extractor import InstructionExtractor
from .caution_generator import CautionGenerator
from .faq_generator import FAQGenerator
from .settings import settings
from .modality_profile import ModalityProfile
from .ocr_temporal_aggregator import OCRTemporalAggregator
from .evidence_fusion import EvidenceFusion

class LLMTrainingAssetBuilder:
    """LLM を使用して source_evidence から training_asset_spec を生成"""
    
    def __init__(self, llm_provider: Optional[LLMProvider] = None):
        """
        Args:
            llm_provider: LLM プロバイダー（デフォルト: settings から選択）
        """
        if llm_provider is None:
            if settings.LLM_PROVIDER_TYPE == "openai":
                llm_provider = OpenAILLMProvider(
                    api_key=settings.OPENAI_API_KEY,
                    model=settings.LLM_MODEL
                )
            else:
                llm_provider = DummyLLMProvider()
        
        self.llm_provider = llm_provider
        self.summary_generator = SummaryGenerator(llm_provider)
        self.instruction_extractor = InstructionExtractor(llm_provider)
        self.caution_generator = CautionGenerator(llm_provider)
        self.faq_generator = FAQGenerator(llm_provider)
    
    def _normalize_instructional_core(self, core: dict) -> dict:
        """Ensure missing structural IDs are added deterministically."""
        chapters = core.get("chapters", [])
        for c_idx, chapter in enumerate(chapters, 1):
            if "chapter_id" not in chapter or not str(chapter["chapter_id"]).strip():
                chapter["chapter_id"] = f"chapter-{c_idx:03d}"
            
            procedures = chapter.get("procedures", [])
            for p_idx, proc in enumerate(procedures, 1):
                if "procedure_id" not in proc or not str(proc["procedure_id"]).strip():
                    proc["procedure_id"] = f"proc-{c_idx:03d}-{p_idx:03d}"
                
                steps = proc.get("steps", [])
                for s_idx, step in enumerate(steps, 1):
                    if "step_id" not in step or not str(step["step_id"]).strip():
                        step["step_id"] = f"step-{c_idx:03d}-{p_idx:03d}-{s_idx:03d}"
                    if "order" not in step:
                        step["order"] = s_idx
        return core

    def build_from_source_evidence(self, source_evidence: Dict[str, Any]) -> Dict[str, Any]:
        """source_evidence から training_asset_spec を生成"""
        
        # Validate source_evidence
        if not source_evidence or "source_video" not in source_evidence:
            raise ValueError("source_evidence must contain source_video")
        
        source_video = source_evidence["source_video"]
        transcript_segments = source_evidence.get("transcript_segments", [])
        ocr_segments = source_evidence.get("ocr_segments", [])
        
        # 1. Modality Profile
        modality_profile = ModalityProfile.from_source_evidence(source_evidence)
        source_evidence["modality_profile"] = modality_profile.to_dict()
        
        # 2. OCR Temporal Aggregation
        aggregator = OCRTemporalAggregator()
        visual_text_segments = aggregator.aggregate(ocr_segments)
        source_evidence["visual_text_segments"] = visual_text_segments
        
        # 3. Evidence Fusion
        fusion = EvidenceFusion(transcript_segments, visual_text_segments, modality_profile)
        evidence_text = fusion.fuse_to_text()
        
        # Generate summaries
        summary = self.summary_generator.generate_summary(evidence_text)
        
        # Extract instructions
        instructional_core = self.instruction_extractor.extract_instructions(evidence_text)
        
        # Post-process to ensure schema stability
        instructional_core = self._normalize_instructional_core(instructional_core)
        
        # Attach screenshots to steps
        from .screenshot_selector import ScreenshotSelector
        selector = ScreenshotSelector(source_evidence)
        for chapter in instructional_core.get("chapters", []):
            for procedure in chapter.get("procedures", []):
                for step in procedure.get("steps", []):
                    screenshot_id = selector.select_for_step(step)
                    if screenshot_id:
                        step["primary_screenshot"] = screenshot_id
        
        # Generate cautions
        cautions = self.caution_generator.generate_cautions(evidence_text)
        
        # Generate FAQs
        faq_candidates = self.faq_generator.generate_faqs(evidence_text, json.dumps(instructional_core, ensure_ascii=False))
        
        # Build training_asset_spec
        asset_id = f"asset-{uuid4().hex[:8]}"
        now = datetime.utcnow().isoformat() + "Z"
        
        training_asset_spec = {
            "asset_meta": {
                "asset_id": asset_id,
                "source_video_id": source_video.get("video_id", "unknown"),
                "title": f"{source_video.get('file_name', 'Training Video')} - LLM 抽出",
                "purpose": summary.get("purpose", ""),
                "target_audience": summary.get("audience", []),
                "target_departments": [],
                "prerequisites": [],
                "language": source_video.get("language", "ja"),
                "status": "draft",
                "version": "0.1.0",
                "created_at": now,
                "updated_at": now
            },
            "source_evidence": {
                "source_video": source_video,
                "transcript_segments": transcript_segments,
                "ocr_segments": source_evidence.get("ocr_segments", []),
                "screenshot_candidates": source_evidence.get("screenshot_candidates", []),
                "speaker_segments": source_evidence.get("speaker_segments", []),
                "evidence_links": source_evidence.get("evidence_links", [])
            },
            "instructional_core": instructional_core,
            "derived_views": {
                "beginner_view": {
                    "key_points": summary.get("outcome", []),
                    "simplified_steps": []
                },
                "checklist_view": {
                    "items": cautions.get("checklist", [])
                },
                "faq_view": {
                    "candidates": faq_candidates
                },
                "manager_view": {
                    "summary": summary.get("purpose", ""),
                    "duration_ms": source_video.get("duration_ms", 0),
                    "prerequisites": [],
                    "competencies": []
                }
            },
            "metadata": {
                "generated_at": now,
                "pipeline_version": "0.6.0",
                "generation_context": "LLM-based extraction",
                "review_status": "pending" if modality_profile.dominant_modality != "weak_evidence" else "needs_review",
                "review_notes": "Generated by LLM; requires human review" if modality_profile.dominant_modality != "weak_evidence" else "Weak evidence detected; heavy human review required",
                "dominant_modality": modality_profile.dominant_modality,
                "evidence_quality": modality_profile.evidence_quality,
                "fusion_mode": fusion.get_fusion_mode()
            }
        }
        
        return training_asset_spec
    
    def build_from_file(self, source_evidence_path: str) -> Dict[str, Any]:
        """ファイルから source_evidence を読み込んで build"""
        with open(source_evidence_path, 'r', encoding='utf-8') as f:
            source_evidence = json.load(f)
        return self.build_from_source_evidence(source_evidence)
    
    def save_training_asset_spec(self, spec: Dict[str, Any], output_path: str) -> None:
        """training_asset_spec をファイルに保存"""
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(spec, f, ensure_ascii=False, indent=2)
