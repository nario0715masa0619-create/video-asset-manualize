"""
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
