"""
Transcript Provider - 動画から文字起こしを取得するための抽象インターフェース
"""

from abc import ABC, abstractmethod
from pathlib import Path
from typing import List, Dict


class TranscriptSegment:
    """文字起こしセグメント"""
    
    def __init__(
        self,
        segment_id: str,
        start_ms: int,
        end_ms: int,
        text: str,
        speaker_id: str = "spk-unknown",
        confidence: float = 1.0
    ):
        self.segment_id = segment_id
        self.start_ms = start_ms
        self.end_ms = end_ms
        self.text = text
        self.speaker_id = speaker_id
        self.confidence = confidence
    
    def to_dict(self) -> dict:
        """Dict に変換"""
        return {
            "segment_id": self.segment_id,
            "start_ms": self.start_ms,
            "end_ms": self.end_ms,
            "text": self.text,
            "speaker_id": self.speaker_id,
            "confidence": self.confidence
        }


class TranscriptProvider(ABC):
    """文字起こし取得プロバイダーの抽象基底クラス"""
    
    @abstractmethod
    def extract_transcript(self, video_path: Path) -> List[TranscriptSegment]:
        """
        動画ファイルから文字起こしを抽出
        
        Args:
            video_path: 動画ファイルのパス
        
        Returns:
            TranscriptSegment のリスト
        """
        pass


class DummyTranscriptProvider(TranscriptProvider):
    """ダミー実装 - テスト用"""
    
    def extract_transcript(self, video_path: Path) -> List[TranscriptSegment]:
        """ダミー文字起こしを返す"""
        return [
            TranscriptSegment(
                segment_id="ts-001",
                start_ms=0,
                end_ms=5000,
                text="これはダミーの文字起こしです。",
                speaker_id="spk-001",
                confidence=0.95
            ),
            TranscriptSegment(
                segment_id="ts-002",
                start_ms=5000,
                end_ms=10000,
                text="実装の確認用データです。",
                speaker_id="spk-001",
                confidence=0.94
            ),
            TranscriptSegment(
                segment_id="ts-003",
                start_ms=10000,
                end_ms=15000,
                text="実際の処理は後で統合予定です。",
                speaker_id="spk-001",
                confidence=0.93
            ),
        ]
