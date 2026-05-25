"""
Frame Extractor - 動画からフレームを抽出
"""

import cv2
from pathlib import Path
from typing import List, Tuple


class FrameExtractor:
    """動画からフレームを抽出"""
    
    @staticmethod
    def extract_frames_by_interval(
        video_path: Path,
        interval_seconds: float = 5.0
    ) -> List[Tuple[int, bytes]]:
        """
        指定間隔でフレームを抽出
        
        Args:
            video_path: 動画ファイルのパス
            interval_seconds: フレーム抽出間隔（秒）
        
        Returns:
            (timestamp_ms, frame_data) のリスト
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            if not cap.isOpened():
                raise RuntimeError(f"Cannot open video: {video_path}")
            
            fps = cap.get(cv2.CAP_PROP_FPS)
            if fps <= 0:
                fps = 30.0
            
            interval_frames = int(fps * interval_seconds)
            if interval_frames <= 0:
                interval_frames = 1
            
            frames = []
            frame_count = 0
            
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                if frame_count % interval_frames == 0:
                    timestamp_ms = int((frame_count / fps) * 1000)
                    frames.append((timestamp_ms, frame))
                
                frame_count += 1
            
            cap.release()
            
            return frames
        
        except ImportError:
            raise RuntimeError(
                "OpenCV not found. Install with: pip install opencv-python"
            )
        except Exception as e:
            raise RuntimeError(f"Frame extraction failed: {str(e)}")
    
    @staticmethod
    def extract_key_frames(
        video_path: Path,
        num_frames: int = 3
    ) -> List[Tuple[int, bytes]]:
        """
        動画から等間隔でキーフレームを抽出
        
        Args:
            video_path: 動画ファイルのパス
            num_frames: 抽出するフレーム数
        
        Returns:
            (timestamp_ms, frame_data) のリスト
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        try:
            cap = cv2.VideoCapture(str(video_path))
            
            if not cap.isOpened():
                raise RuntimeError(f"Cannot open video: {video_path}")
            
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            
            if fps <= 0:
                fps = 30.0
            
            if total_frames <= 0:
                raise RuntimeError("Cannot determine video length")
            
            interval = max(1, total_frames // num_frames)
            frames = []
            
            for i in range(num_frames):
                frame_idx = i * interval
                cap.set(cv2.CAP_PROP_POS_FRAMES, frame_idx)
                ret, frame = cap.read()
                
                if ret:
                    timestamp_ms = int((frame_idx / fps) * 1000)
                    frames.append((timestamp_ms, frame))
            
            cap.release()
            
            return frames
        
        except ImportError:
            raise RuntimeError(
                "OpenCV not found. Install with: pip install opencv-python"
            )
        except Exception as e:
            raise RuntimeError(f"Key frame extraction failed: {str(e)}")
