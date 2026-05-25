"""
Phase 4 実装自動生成スクリプト
ffprobe メタデータ取得と Whisper STT 統合
"""

from pathlib import Path

# ========== 1. ffprobe_metadata_extractor.py ==========
ffprobe_code = r'''"""
FFprobe Metadata Extractor - 動画ファイルからメタデータを取得
"""

import json
import subprocess
from pathlib import Path
from typing import Dict, Optional


class FFprobeMetadataExtractor:
    """ffprobe を使った動画メタデータ抽出"""
    
    @staticmethod
    def extract_metadata(video_path: Path) -> Dict:
        """
        ffprobe で動画メタデータを取得
        
        Args:
            video_path: 動画ファイルのパス
        
        Returns:
            メタデータ dict
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        try:
            # ffprobe コマンドを実行
            cmd = [
                "ffprobe",
                "-v", "error",
                "-show_format",
                "-show_streams",
                "-of", "json",
                str(video_path)
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"ffprobe failed: {result.stderr}")
            
            probe_data = json.loads(result.stdout)
            
            # メタデータを抽出
            metadata = FFprobeMetadataExtractor._parse_probe_data(
                probe_data,
                video_path
            )
            
            return metadata
        
        except FileNotFoundError:
            raise RuntimeError(
                "ffprobe not found. "
                "Please install ffmpeg: "
                "https://ffmpeg.org/download.html"
            )
        except Exception as e:
            raise RuntimeError(f"Metadata extraction failed: {str(e)}")
    
    @staticmethod
    def _parse_probe_data(probe_data: dict, video_path: Path) -> Dict:
        """ffprobe の出力をパース"""
        format_info = probe_data.get("format", {})
        streams = probe_data.get("streams", [])
        
        # 動画ストリームを探す
        video_stream = None
        audio_stream = None
        
        for stream in streams:
            if stream.get("codec_type") == "video" and not video_stream:
                video_stream = stream
            elif stream.get("codec_type") == "audio" and not audio_stream:
                audio_stream = stream
        
        # Duration (ms に変換)
        duration_sec = float(format_info.get("duration", 0))
        duration_ms = int(duration_sec * 1000)
        
        # 解像度
        width = video_stream.get("width", 0) if video_stream else 0
        height = video_stream.get("height", 0) if video_stream else 0
        
        # FPS
        fps_str = video_stream.get("r_frame_rate", "30/1") if video_stream else "30/1"
        try:
            num, den = map(float, fps_str.split("/"))
            fps = num / den if den != 0 else 30.0
        except:
            fps = 30.0
        
        # Audio の有無
        has_audio = audio_stream is not None
        
        return {
            "file_name": video_path.name,
            "file_path": str(video_path.absolute()),
            "duration_ms": duration_ms,
            "width": width,
            "height": height,
            "fps": fps,
            "has_audio": has_audio,
            "codec": video_stream.get("codec_name", "unknown") if video_stream else "unknown"
        }
'''

# ========== 2. whisper_transcript_provider.py ==========
whisper_code = r'''"""
Whisper Transcript Provider - OpenAI Whisper を使った STT
"""

import json
import subprocess
import tempfile
from pathlib import Path
from typing import List
import re

from .transcript_provider import TranscriptProvider, TranscriptSegment


class WhisperTranscriptProvider(TranscriptProvider):
    """OpenAI Whisper を使った文字起こし"""
    
    def __init__(self, model: str = "base", language: str = "ja"):
        """
        Initialize Whisper provider
        
        Args:
            model: Whisper model (tiny, base, small, medium, large)
            language: Language code (e.g., 'ja', 'en')
        """
        self.model = model
        self.language = language
    
    def extract_transcript(self, video_path: Path) -> List[TranscriptSegment]:
        """
        Whisper で動画から文字起こしを抽出
        
        Args:
            video_path: 動画ファイルのパス
        
        Returns:
            TranscriptSegment のリスト
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        try:
            # Whisper を実行
            with tempfile.NamedTemporaryFile(
                suffix=".json",
                delete=False
            ) as tmp:
                output_file = tmp.name
            
            cmd = [
                "whisper",
                str(video_path),
                "--model", self.model,
                "--language", self.language,
                "--output_format", "json",
                "--output_dir", Path(output_file).parent.as_posix()
            ]
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=600  # 10 分タイムアウト
            )
            
            if result.returncode != 0:
                raise RuntimeError(f"Whisper failed: {result.stderr}")
            
            # JSON 出力を読み込み
            json_file = Path(output_file).parent / (
                Path(video_path).stem + ".json"
            )
            
            if not json_file.exists():
                raise FileNotFoundError(f"Whisper output not found: {json_file}")
            
            with open(json_file, "r", encoding="utf-8") as f:
                whisper_output = json.load(f)
            
            # TranscriptSegment に変換
            segments = self._parse_whisper_output(whisper_output)
            
            # クリーンアップ
            json_file.unlink(missing_ok=True)
            
            return segments
        
        except FileNotFoundError as e:
            if "whisper" in str(e).lower():
                raise RuntimeError(
                    "Whisper not found. "
                    "Install with: pip install openai-whisper"
                )
            raise
        except Exception as e:
            raise RuntimeError(f"Transcript extraction failed: {str(e)}")
    
    @staticmethod
    def _parse_whisper_output(output: dict) -> List[TranscriptSegment]:
        """Whisper の JSON 出力をパース"""
        segments = []
        
        for i, segment in enumerate(output.get("segments", [])):
            seg = TranscriptSegment(
                segment_id=f"ts-{i+1:03d}",
                start_ms=int(segment.get("start", 0) * 1000),
                end_ms=int(segment.get("end", 0) * 1000),
                text=segment.get("text", "").strip(),
                speaker_id="spk-001",
                confidence=segment.get("confidence", 0.95)
            )
            segments.append(seg)
        
        return segments
'''

# ========== 3. provider_factory.py ==========
factory_code = r'''"""
Provider Factory - Provider の生成と切り替え
"""

from typing import Literal
from .transcript_provider import (
    TranscriptProvider,
    DummyTranscriptProvider
)
from .ocr_provider import OCRProvider, DummyOCRProvider


class ProviderFactory:
    """Provider ファクトリ"""
    
    @staticmethod
    def create_transcript_provider(
        provider_type: Literal["dummy", "whisper"] = "dummy",
        **kwargs
    ) -> TranscriptProvider:
        """
        Transcript Provider を生成
        
        Args:
            provider_type: "dummy" または "whisper"
            **kwargs: Provider に渡すオプション
        
        Returns:
            TranscriptProvider インスタンス
        """
        if provider_type == "whisper":
            try:
                from .whisper_transcript_provider import WhisperTranscriptProvider
                return WhisperTranscriptProvider(
                    model=kwargs.get("model", "base"),
                    language=kwargs.get("language", "ja")
                )
            except ImportError:
                raise ImportError(
                    "Whisper provider requires openai-whisper. "
                    "Install with: pip install openai-whisper"
                )
        else:
            return DummyTranscriptProvider()
    
    @staticmethod
    def create_ocr_provider(
        provider_type: Literal["dummy", "easyocr"] = "dummy",
        **kwargs
    ) -> OCRProvider:
        """
        OCR Provider を生成
        
        Args:
            provider_type: "dummy" または "easyocr"
            **kwargs: Provider に渡すオプション
        
        Returns:
            OCRProvider インスタンス
        """
        return DummyOCRProvider()
'''

# ファイルを作成
src_dir = Path("src/video_asset_manualize")

files = {
    "ffprobe_metadata_extractor.py": ffprobe_code,
    "whisper_transcript_provider.py": whisper_code,
    "provider_factory.py": factory_code,
}

for filename, content in files.items():
    file_path = src_dir / filename
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)
    print(f"✓ Created: {file_path}")

print("\n✅ Phase 4 基盤モジュール作成完了")
