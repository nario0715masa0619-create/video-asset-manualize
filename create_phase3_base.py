"""
Phase 3 最小実装自動生成スクリプト
"""

from pathlib import Path
import json

# ========== 1. transcript_provider.py ==========
transcript_provider = r'''"""
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
'''

# ========== 2. ocr_provider.py ==========
ocr_provider = r'''"""
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
    def extract_ocr(self, video_path: Path) -> List[OCRSegment]:
        """
        動画フレームから OCR を抽出
        
        Args:
            video_path: 動画ファイルのパス
        
        Returns:
            OCRSegment のリスト
        """
        pass


class DummyOCRProvider(OCRProvider):
    """ダミー実装 - テスト用"""
    
    def extract_ocr(self, video_path: Path) -> List[OCRSegment]:
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
'''

# ========== 3. video_source_evidence_builder.py ==========
video_source_evidence_builder = r'''"""
Video Source Evidence Builder
動画ファイルから source_evidence を生成するビルダー
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from .transcript_provider import TranscriptProvider, DummyTranscriptProvider
from .ocr_provider import OCRProvider, DummyOCRProvider


class VideoSourceEvidenceBuilder:
    """動画ファイルから source_evidence を生成"""
    
    def __init__(
        self,
        transcript_provider: Optional[TranscriptProvider] = None,
        ocr_provider: Optional[OCRProvider] = None
    ):
        """
        Initialize builder with providers
        
        Args:
            transcript_provider: 文字起こしプロバイダー (デフォルト: Dummy)
            ocr_provider: OCR プロバイダー (デフォルト: Dummy)
        """
        self.transcript_provider = transcript_provider or DummyTranscriptProvider()
        self.ocr_provider = ocr_provider or DummyOCRProvider()
        self.source_evidence = None
    
    def build_from_video(self, video_path: Path) -> dict:
        """
        動画ファイルから source_evidence を生成
        
        Args:
            video_path: 動画ファイルのパス
        
        Returns:
            source_evidence dict
        """
        video_path = Path(video_path)
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        # source_video メタデータを構築
        source_video = {
            "video_id": f"video-{video_path.stem}",
            "file_name": video_path.name,
            "file_path": str(video_path),
            "source_type": "local_file",
            "duration_ms": 0,  # 実装では ffprobe で取得
            "language": "ja",
            "checksum": None
        }
        
        # Transcript を抽出
        transcript_segments = []
        try:
            segments = self.transcript_provider.extract_transcript(video_path)
            transcript_segments = [seg.to_dict() for seg in segments]
        except Exception as e:
            print(f"Warning: Transcript extraction failed: {e}")
        
        # OCR を抽出
        ocr_segments = []
        try:
            segments = self.ocr_provider.extract_ocr(video_path)
            ocr_segments = [seg.to_dict() for seg in segments]
        except Exception as e:
            print(f"Warning: OCR extraction failed: {e}")
        
        # source_evidence を構築
        self.source_evidence = {
            "source_video": source_video,
            "transcript_segments": transcript_segments,
            "ocr_segments": ocr_segments,
            "screenshot_candidates": [],
            "speaker_segments": [],
            "evidence_links": []
        }
        
        return self.source_evidence
    
    def save_to_file(self, output_path: Path) -> Path:
        """
        source_evidence をファイルに保存
        
        Args:
            output_path: 出力ファイルのパス
        
        Returns:
            保存されたファイルのパス
        """
        if not self.source_evidence:
            raise ValueError("No source_evidence generated yet")
        
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, "w", encoding="utf-8") as f:
            json.dump(self.source_evidence, f, indent=2, ensure_ascii=False)
        
        return output_path
'''

# ファイルを作成
src_dir = Path("src/video_asset_manualize")

files = {
    "transcript_provider.py": transcript_provider,
    "ocr_provider.py": ocr_provider,
    "video_source_evidence_builder.py": video_source_evidence_builder,
}

for filename, content in files.items():
    file_path = src_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Created: {file_path}")

print("\n✅ Phase 3 基盤モジュール作成完了")
