"""
Screenshot Selector - Step に対応する最適なスクリーンショットを選定する
"""

from typing import Dict, Any, List, Optional
import math

class ScreenshotSelector:
    """Step にスクリーンショットを割り当てるクラス"""
    
    def __init__(self, source_evidence: Dict[str, Any]):
        """
        Args:
            source_evidence: 抽出された証拠データ (screenshot_candidates を含む)
        """
        self.source_evidence = source_evidence
        self.screenshot_candidates = source_evidence.get("screenshot_candidates", [])
        
        # Build evidence timestamp lookup
        self.evidence_timestamps = {}
        
        for ts in source_evidence.get("transcript_segments", []):
            self.evidence_timestamps[ts["segment_id"]] = ts.get("start_ms", 0)
            
        for ocr in source_evidence.get("ocr_segments", []):
            self.evidence_timestamps[ocr["ocr_id"]] = ocr.get("start_ms", 0)
            
        # Used screenshots tracker to encourage variety
        self.used_screenshots = set()

    def select_for_step(self, step: Dict[str, Any]) -> Optional[str]:
        """
        Step に最適なスクリーンショットの ID を選定して返す
        
        Args:
            step: 処理対象の step
            
        Returns:
            最適な screenshot_id、存在しない場合は None
        """
        if not self.screenshot_candidates:
            return None
            
        evidence_refs = step.get("evidence_refs", [])
        if not evidence_refs:
            # Fallback: if no evidence refs, just return None or first available
            return None
            
        # 1. Step に関連する証拠の平均タイムスタンプを計算
        target_timestamps = []
        for ref in evidence_refs:
            if ref in self.evidence_timestamps:
                target_timestamps.append(self.evidence_timestamps[ref])
                
        if not target_timestamps:
            return None
            
        target_ts = sum(target_timestamps) / len(target_timestamps)
        
        # 2. 最も近いスクリーンショットを探す
        best_candidate = None
        min_distance = float('inf')
        
        # 優先的に未使用のスクリーンショットを選ぶためのペナルティ
        USED_PENALTY_MS = 2000  # 2秒分のペナルティ
        
        for candidate in self.screenshot_candidates:
            cand_ts = candidate.get("timestamp_ms", 0)
            distance = abs(cand_ts - target_ts)
            
            if candidate["screenshot_id"] in self.used_screenshots:
                distance += USED_PENALTY_MS
                
            if distance < min_distance:
                min_distance = distance
                best_candidate = candidate
                
        if best_candidate:
            self.used_screenshots.add(best_candidate["screenshot_id"])
            return best_candidate["screenshot_id"]
            
        return None
