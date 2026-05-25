"""
video_source_evidence_builder.py を修正
ffprobe メタデータ取得と Provider Factory 統合
"""

from pathlib import Path

builder_file = Path("src/video_asset_manualize/video_source_evidence_builder.py")

new_code = r'''"""
Video Source Evidence Builder
動画ファイルから source_evidence を生成するビルダー
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Optional

from .transcript_provider import TranscriptProvider, DummyTranscriptProvider
from .ocr_provider import OCRProvider, DummyOCRProvider
from .provider_factory import ProviderFactory
from .ffprobe_metadata_extractor import FFprobeMetadataExtractor
from .settings import settings


class VideoSourceEvidenceBuilder:
    """動画ファイルから source_evidence を生成"""
    
    def __init__(
        self,
        transcript_provider: Optional[TranscriptProvider] = None,
        ocr_provider: Optional[OCRProvider] = None,
        extract_metadata: bool = True
    ):
        """
        Initialize builder with providers
        
        Args:
            transcript_provider: 文字起こしプロバイダー (デフォルト: settings から取得)
            ocr_provider: OCR プロバイダー (デフォルト: Dummy)
            extract_metadata: ffprobe でメタデータを取得するか
        """
        # Provider を初期化
        if transcript_provider is None:
            self.transcript_provider = ProviderFactory.create_transcript_provider(
                provider_type=settings.TRANSCRIPT_PROVIDER_TYPE,
                model=settings.WHISPER_MODEL,
                language=settings.WHISPER_LANGUAGE
            )
        else:
            self.transcript_provider = transcript_provider
        
        if ocr_provider is None:
            self.ocr_provider = ProviderFactory.create_ocr_provider(
                provider_type=settings.OCR_PROVIDER_TYPE
            )
        else:
            self.ocr_provider = ocr_provider
        
        self.extract_metadata = extract_metadata
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
        source_video = self._extract_source_video_metadata(video_path)
        
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
    
    def _extract_source_video_metadata(self, video_path: Path) -> dict:
        """
        source_video メタデータを抽出
        
        Args:
            video_path: 動画ファイルのパス
        
        Returns:
            source_video dict
        """
        video_path = Path(video_path)
        
        # 基本情報
        source_video = {
            "video_id": f"video-{video_path.stem}",
            "file_name": video_path.name,
            "file_path": str(video_path.absolute()),
            "source_type": "local_file",
            "duration_ms": 0,
            "language": "ja",
            "checksum": None
        }
        
        # ffprobe でメタデータを取得
        if self.extract_metadata:
            try:
                extractor = FFprobeMetadataExtractor()
                metadata = extractor.extract_metadata(video_path)
                
                source_video["duration_ms"] = metadata.get("duration_ms", 0)
                source_video["width"] = metadata.get("width", 0)
                source_video["height"] = metadata.get("height", 0)
                source_video["fps"] = metadata.get("fps", 30.0)
                source_video["has_audio"] = metadata.get("has_audio", False)
                
            except Exception as e:
                print(f"Warning: Metadata extraction failed: {e}")
                print("         Using default values")
        
        return source_video
    
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

with open(builder_file, "w", encoding="utf-8") as f:
    f.write(new_code)

print("✓ video_source_evidence_builder.py を修正しました")
