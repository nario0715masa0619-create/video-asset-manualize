"""
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
