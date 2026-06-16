"""
Evidence Fusion - Fuses transcript and OCR visual text based on dominant modality.
"""
from typing import List, Dict, Any
from .modality_profile import ModalityProfile

class EvidenceFusion:
    def __init__(self, transcript_segments: List[Dict[str, Any]], visual_text_segments: List[Dict[str, Any]], modality_profile: ModalityProfile):
        self.transcript_segments = transcript_segments
        self.visual_text_segments = visual_text_segments
        self.modality_profile = modality_profile
        
    def get_fusion_mode(self) -> str:
        dominant = self.modality_profile.dominant_modality
        if dominant == "speech_dominant":
            return "transcript_primary_ocr_secondary"
        elif dominant == "text_dominant":
            return "ocr_primary_transcript_secondary"
        elif dominant == "mixed":
            return "interleaved"
        else:
            return "weak_evidence"
            
    def fuse_to_text(self) -> str:
        """
        Creates a unified chronological text representation of the evidence for the LLM.
        """
        mode = self.get_fusion_mode()
        
        # Combine all events into a single timeline
        timeline = []
        for t in self.transcript_segments:
            timeline.append({
                "type": "SPEECH",
                "start": t.get("start_ms", 0),
                "end": t.get("end_ms", 0),
                "text": t.get("text", "")
            })
            
        for v in self.visual_text_segments:
            timeline.append({
                "type": "ON_SCREEN_TEXT",
                "start": v.get("start_ms", 0),
                "end": v.get("end_ms", 0),
                "text": v.get("text", "")
            })
            
        # Sort by start_ms
        timeline.sort(key=lambda x: x["start"])
        
        output_lines = [
            f"--- EVIDENCE FUSION LOG ---",
            f"Dominant Modality: {self.modality_profile.dominant_modality}",
            f"Evidence Quality: {self.modality_profile.evidence_quality}",
            f"Fusion Mode: {mode}",
            "---------------------------"
        ]
        
        if not timeline:
            output_lines.append("(No evidence available)")
            return "\n".join(output_lines)
            
        for event in timeline:
            start_sec = event["start"] / 1000.0
            end_sec = event["end"] / 1000.0
            
            # Highlight importance based on modality
            prefix = ""
            if mode == "transcript_primary_ocr_secondary" and event["type"] == "SPEECH":
                prefix = "[PRIMARY] "
            elif mode == "ocr_primary_transcript_secondary" and event["type"] == "ON_SCREEN_TEXT":
                prefix = "[PRIMARY] "
                
            output_lines.append(f"[{start_sec:.1f}s - {end_sec:.1f}s] {event['type']}: {prefix}{event['text']}")
            
        return "\n".join(output_lines)
