"""
Modality Profile - VAM Evidence-first Redesign
Analyzes source evidence to determine the dominant modality and evidence quality.
"""
from typing import Dict, Any

class ModalityProfile:
    def __init__(
        self,
        transcript_segment_count: int,
        transcript_total_chars: int,
        ocr_block_count: int,
        ocr_total_chars: int
    ):
        self.transcript_segment_count = transcript_segment_count
        self.transcript_total_chars = transcript_total_chars
        self.ocr_block_count = ocr_block_count
        self.ocr_total_chars = ocr_total_chars
        
        self.dominant_modality = self._determine_dominant_modality()
        self.evidence_quality = self._determine_evidence_quality()

    def _determine_dominant_modality(self) -> str:
        transcript_strong = self.transcript_total_chars >= 50
        ocr_strong = self.ocr_total_chars >= 50
        
        # If very highly skewed towards one modality
        if transcript_strong and self.transcript_total_chars > self.ocr_total_chars * 5:
            return "speech_dominant"
        if ocr_strong and self.ocr_total_chars > self.transcript_total_chars * 5:
            return "text_dominant"
            
        if transcript_strong and ocr_strong:
            return "mixed"
        elif transcript_strong:
            return "speech_dominant"
        elif ocr_strong:
            return "text_dominant"
        else:
            return "weak_evidence"

    def _determine_evidence_quality(self) -> str:
        total_chars = self.transcript_total_chars + self.ocr_total_chars
        if total_chars >= 200:
            return "strong"
        elif total_chars >= 50:
            return "medium"
        else:
            return "weak"

    @classmethod
    def from_source_evidence(cls, source_evidence: Dict[str, Any]) -> "ModalityProfile":
        transcript_segments = source_evidence.get("transcript_segments", [])
        ocr_segments = source_evidence.get("ocr_segments", [])
        
        transcript_count = len(transcript_segments)
        transcript_chars = sum(len(seg.get("text", "").strip()) for seg in transcript_segments)
        
        ocr_count = len(ocr_segments)
        ocr_chars = sum(len(seg.get("text", "").strip()) for seg in ocr_segments)
        
        return cls(
            transcript_segment_count=transcript_count,
            transcript_total_chars=transcript_chars,
            ocr_block_count=ocr_count,
            ocr_total_chars=ocr_chars
        )
        
    def to_dict(self) -> Dict[str, Any]:
        return {
            "transcript_segment_count": self.transcript_segment_count,
            "transcript_total_chars": self.transcript_total_chars,
            "ocr_block_count": self.ocr_block_count,
            "ocr_total_chars": self.ocr_total_chars,
            "dominant_modality": self.dominant_modality,
            "evidence_quality": self.evidence_quality
        }
