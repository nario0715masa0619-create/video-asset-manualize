"""
Phase 6 デバッグスクリプト - 詳細エラー出力
"""

from pathlib import Path
import json
import traceback

try:
    from video_asset_manualize.build_training_asset_pipeline import BuildTrainingAssetPipeline
    
    pipeline = BuildTrainingAssetPipeline()
    results = pipeline.generate_outputs(
        "output/exports/phase6_spec_dummy.json",
        output_dir="output/exports",
        format="all"
    )
    
    print("Success!")
    for k, v in results.items():
        print(f"{k}: {v}")
        
except Exception as e:
    print(f"Error: {str(e)}")
    traceback.print_exc()
