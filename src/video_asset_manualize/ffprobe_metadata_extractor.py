"""
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
