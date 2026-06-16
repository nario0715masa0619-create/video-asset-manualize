"""
OCR Temporal Aggregator - Groups continuous similar OCR text into consolidated segments.
"""
from typing import List, Dict, Any
import difflib
import uuid

class OCRTemporalAggregator:
    def __init__(self, gap_tolerance_ms: int = 500, similarity_threshold: float = 0.8):
        self.gap_tolerance_ms = gap_tolerance_ms
        self.similarity_threshold = similarity_threshold

    def aggregate(self, ocr_segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """
        Aggregates raw OCR segments into contiguous visual text segments.
        """
        if not ocr_segments:
            return []
            
        # Sort segments by start time
        sorted_segments = sorted(ocr_segments, key=lambda x: x.get("start_ms", 0))
        
        aggregated = []
        current_cluster = [sorted_segments[0]]
        
        for i in range(1, len(sorted_segments)):
            seg = sorted_segments[i]
            prev_seg = current_cluster[-1]
            
            time_gap = seg.get("start_ms", 0) - prev_seg.get("end_ms", 0)
            
            # If within gap and similar text, cluster them
            if time_gap <= self.gap_tolerance_ms and self._is_similar(seg.get("text", ""), prev_seg.get("text", "")):
                current_cluster.append(seg)
            else:
                aggregated.append(self._build_segment(current_cluster))
                current_cluster = [seg]
                
        if current_cluster:
            aggregated.append(self._build_segment(current_cluster))
            
        return aggregated

    def _is_similar(self, text1: str, text2: str) -> bool:
        if not text1 or not text2:
            return False
        # Normalize simple spacing/casing
        t1 = text1.strip().lower()
        t2 = text2.strip().lower()
        if t1 == t2:
            return True
        ratio = difflib.SequenceMatcher(None, t1, t2).ratio()
        return ratio >= self.similarity_threshold

    def _build_segment(self, cluster: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Builds a consolidated visual_text_segment from a cluster of raw ocr_segments.
        """
        # Start is the first frame's start, end is the last frame's end
        start_ms = cluster[0].get("start_ms", 0)
        end_ms = cluster[-1].get("end_ms", cluster[-1].get("start_ms", 0))
        
        # Pick the longest text as representative (or most confident)
        best_seg = max(cluster, key=lambda x: len(x.get("text", "").strip()) * x.get("confidence", 0.5))
        
        # Average confidence
        confidences = [s.get("confidence", 0) for s in cluster if "confidence" in s]
        avg_confidence = sum(confidences) / len(confidences) if confidences else 0.0
        
        source_frames = [s.get("ocr_id") for s in cluster if "ocr_id" in s]
        
        return {
            "segment_id": f"vts-{uuid.uuid4().hex[:8]}",
            "start_ms": start_ms,
            "end_ms": end_ms,
            "text": best_seg.get("text", ""),
            "confidence": avg_confidence,
            "bbox": best_seg.get("bbox", []),
            "source_frames": source_frames,
            "text_role": "unknown"  # Can be enhanced later
        }
