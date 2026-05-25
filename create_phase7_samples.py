"""
Phase 7 サンプル Manifest 作成スクリプト
"""

from pathlib import Path
import json

# ========== サンプル動画 manifest ==========
videos_manifest = {
    "project_id": "project-training-001",
    "title": "Customer Service Training Series",
    "description": "Complete training for customer registration and support procedures",
    "items": [
        {
            "video_id": "video-001",
            "input_path": "samples/sample_training_video.mp4",
            "title": "Customer Registration Basics",
            "audience": ["New Employees", "Store Staff"]
        },
        {
            "video_id": "video-002",
            "input_path": "samples/sample_training_video.mp4",
            "title": "Advanced Customer Management",
            "audience": ["Staff", "Managers"]
        }
    ]
}

# ========== サンプル spec manifest ==========
specs_manifest = {
    "project_id": "project-training-001",
    "title": "Customer Service Training Series",
    "items": [
        {
            "asset_id": "asset-001",
            "spec_path": "output/exports/phase6_spec_dummy.json",
            "title": "Customer Registration Manual"
        }
    ]
}

# 保存
samples_dir = Path("samples")
samples_dir.mkdir(exist_ok=True)

with open(samples_dir / "videos_manifest.json", 'w', encoding='utf-8') as f:
    json.dump(videos_manifest, f, ensure_ascii=False, indent=2)
print("OK: samples/videos_manifest.json")

with open(samples_dir / "specs_manifest.json", 'w', encoding='utf-8') as f:
    json.dump(specs_manifest, f, ensure_ascii=False, indent=2)
print("OK: samples/specs_manifest.json")

print("\nOK: Sample manifests created")
