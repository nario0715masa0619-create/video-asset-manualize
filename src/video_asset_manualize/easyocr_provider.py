"""
EasyOCR Provider - EasyOCR を使った OCR 実装
"""

from pathlib import Path
from typing import List
import numpy as np

from .ocr_provider import OCRProvider, OCRSegment


class EasyOCRProvider(OCRProvider):
    """EasyOCR を使った OCR プロバイダー"""
    
    def __init__(self, languages: List[str] = None, gpu: bool = False):
        """
        Initialize EasyOCR provider
        
        Args:
            languages: OCR 対象言語 (デフォルト: ['ja', 'en'])
            gpu: GPU を使用するか
        """
        self.languages = languages or ['ja', 'en']
        self.gpu = gpu
        self.reader = None
        self._initialize_reader()
    
    def _initialize_reader(self):
        """EasyOCR reader を初期化"""
        try:
            import easyocr
            self.reader = easyocr.Reader(self.languages, gpu=self.gpu)
        except ImportError:
            raise ImportError(
                "EasyOCR not found. Install with: pip install easyocr"
            )
        except Exception as e:
            raise RuntimeError(f"EasyOCR initialization failed: {str(e)}")
    
    def extract_ocr(self, video_path: Path) -> List[OCRSegment]:
        """
        動画から OCR を抽出
        
        Args:
            video_path: 動画ファイルのパス
        
        Returns:
            OCRSegment のリスト
        """
        video_path = Path(video_path)
        
        if not video_path.exists():
            raise FileNotFoundError(f"Video file not found: {video_path}")
        
        try:
            from .frame_extractor import FrameExtractor
            
            # 動画からキーフレームを抽出
            frames = FrameExtractor.extract_key_frames(
                video_path,
                num_frames=3
            )
            
            ocr_segments = []
            segment_id_counter = 1
            
            for timestamp_ms, frame in frames:
                # EasyOCR で OCR を実行
                results = self.reader.readtext(frame)
                
                # 結果をパース
                for result in results:
                    bbox, text, confidence = result
                    
                    # bbox を [x1, y1, x2, y2] 形式に変換
                    bbox_normalized = self._normalize_bbox(bbox)
                    
                    ocr_seg = OCRSegment(
                        ocr_id=f"ocr-{segment_id_counter:03d}",
                        start_ms=timestamp_ms,
                        end_ms=timestamp_ms,
                        text=text.strip(),
                        bbox=bbox_normalized,
                        confidence=float(confidence)
                    )
                    
                    ocr_segments.append(ocr_seg)
                    segment_id_counter += 1
            
            return ocr_segments
        
        except Exception as e:
            raise RuntimeError(f"OCR extraction failed: {str(e)}")
    
    @staticmethod
    def _normalize_bbox(bbox) -> List[float]:
        """
        EasyOCR の bbox を [x1, y1, x2, y2] に正規化
        
        Args:
            bbox: EasyOCR の bbox ((x1,y1), (x2,y2), (x3,y3), (x4,y4))
        
        Returns:
            [x1, y1, x2, y2] 形式
        """
        if isinstance(bbox, (list, tuple)) and len(bbox) >= 2:
            points = np.array(bbox, dtype=np.float32)
            x_coords = points[:, 0]
            y_coords = points[:, 1]
            
            x1 = float(np.min(x_coords))
            y1 = float(np.min(y_coords))
            x2 = float(np.max(x_coords))
            y2 = float(np.max(y_coords))
            
            return [x1, y1, x2, y2]
        
        return [0, 0, 0, 0]
