"""
UI Pipeline Runner - CLI パイプラインを UI から呼び出すラッパー
Phase 9: UI から直接実行可能にする
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import json
from datetime import datetime

from video_asset_manualize.video_source_evidence_builder import VideoSourceEvidenceBuilder
from video_asset_manualize.source_evidence_to_training_asset_builder import SourceEvidenceToTrainingAssetBuilder
from video_asset_manualize.build_training_asset_pipeline import BuildTrainingAssetPipeline


class UIExecutionResult:
    """UI 実行結果を統一的に管理"""

    def __init__(self):
        self.success = False
        self.message = ""
        self.error_message = ""
        self.files = {}  # {file_type: file_path}
        self.asset_id = None
        self.logs = []

    def add_log(self, message: str):
        """ログ追加"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.logs.append(f"[{timestamp}] {message}")


class UIPipelineRunner:
    """UIからの実行を管理するランナークラス"""
    
    def __init__(self):
        self.output_dir = Path("output/exports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def run_single_video(self, video_path: str, use_llm: bool, llm_provider: str, transcript_provider: str, ocr_provider: str) -> UIExecutionResult:
        result = UIExecutionResult()
        
        try:
            result.add_log("Step 1: Extracting source evidence...")
            evidence_builder = VideoSourceEvidenceBuilder()
            source_evidence = evidence_builder.build_from_video(video_path)
            result.add_log("Source evidence extracted successfully.")
            
            result.add_log("Step 2: Building training asset spec...")
            spec_builder = SourceEvidenceToTrainingAssetBuilder()
            spec = spec_builder.build_from_source_evidence(source_evidence)
            result.add_log("Spec built successfully.")
            
            result.add_log("Step 3: Generating HTML/PDF outputs...")
            asset_id = spec.get('asset_meta', {}).get('asset_id', 'unknown')
            result.asset_id = asset_id
            
            spec_file = self.output_dir / f"{asset_id}_spec.json"
            with open(spec_file, 'w', encoding='utf-8') as f:
                json.dump(spec, f, ensure_ascii=False, indent=2)
                
            pipeline = BuildTrainingAssetPipeline()
            outputs = pipeline.generate_outputs(str(spec_file), output_dir=str(self.output_dir))
            
            result.success = True
            result.message = "Processing complete!"
            result.files = outputs
            result.add_log("Pipeline completed successfully.")
            
        except Exception as e:
            result.success = False
            result.error_message = str(e)
            result.add_log(f"Error occurred: {str(e)}")
            
        return result
