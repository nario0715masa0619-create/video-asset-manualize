"""
OCR Provider - 動画フレームから OCR を実行するための抽象インターフェース
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict, Tuple


class OCRSegment:
    """OCR セグメント"""
    
    def __init__(
        self,
        ocr_id: str,
        start_ms: int,
        end_ms: int,
        text: str,
        bbox: List[float] = None,
        confidence: float = 1.0
    ):
        self.ocr_id = ocr_id
        self.start_ms = start_ms
        self.end_ms = end_ms
        self.text = text
        self.bbox = bbox or [0, 0, 0, 0]
        self.confidence = confidence
    
    def to_dict(self) -> dict:
        """Dict に変換"""
        return {
            "ocr_id": self.ocr_id,
            "start_ms": self.start_ms,
            "end_ms": self.end_ms,
            "text": self.text,
            "bbox": self.bbox,
            "confidence": self.confidence
        }


class OCRProvider(ABC):
    """OCR プロバイダーの抽象基底クラス"""
    
    @abstractmethod
    def extract_ocr(self, video_path: Path, screenshot_candidates: List[Dict] = None) -> List[OCRSegment]:
        """
        動画フレームから OCR を抽出
        
        Args:
            video_path: 動画ファイルのパス
            screenshot_candidates: 事前抽出されたスクリーンショット候補（任意）
        
        Returns:
            OCRSegment のリスト
        """
        pass


class DummyOCRProvider(OCRProvider):
    """ダミー実装 - テスト用"""
    
    def extract_ocr(self, video_path: Path, screenshot_candidates: List[Dict] = None) -> List[OCRSegment]:
        """ダミー OCR テキストを返す"""
        return [
            OCRSegment(
                ocr_id="ocr-001",
                start_ms=2000,
                end_ms=5000,
                text="メニュー画面",
                bbox=[100, 50, 300, 100],
                confidence=0.92
            ),
            OCRSegment(
                ocr_id="ocr-002",
                start_ms=8000,
                end_ms=12000,
                text="確認ボタン",
                bbox=[400, 400, 600, 450],
                confidence=0.91
            ),
        ]
