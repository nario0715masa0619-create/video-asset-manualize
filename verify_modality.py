import json
from pathlib import Path
import os
import subprocess

def create_mock_evidence():
    base_dir = Path("samples/mock_evidences")
    base_dir.mkdir(parents=True, exist_ok=True)
    
    # 1. Speech Dominant
    speech = {
        "source_video": {"video_id": "v-speech", "file_name": "speech.mp4", "file_path": "/tmp/speech.mp4", "source_type": "local_file", "duration_ms": 10000, "language": "ja"},
        "transcript_segments": [
            {"segment_id": f"ts-{i}", "start_ms": i*1000, "end_ms": (i+1)*1000, "text": "音声のみで説明しています" * 5, "confidence": 0.9} for i in range(5)
        ]
    }
    with open(base_dir / "speech.json", 'w', encoding='utf-8') as f: json.dump(speech, f, ensure_ascii=False)
        
    # 2. Text Dominant
    text = {
        "source_video": {"video_id": "v-text", "file_name": "text.mp4", "file_path": "/tmp/text.mp4", "source_type": "local_file", "duration_ms": 10000, "language": "ja"},
        "transcript_segments": [],
        "ocr_segments": [
            {"ocr_id": f"ocr-{i}", "start_ms": i*1000, "end_ms": i*1000, "text": "画面上の文字です。これがたくさんあります。" * 5, "bbox": [0,0,10,10], "confidence": 0.9} for i in range(5)
        ]
    }
    with open(base_dir / "text.json", 'w', encoding='utf-8') as f: json.dump(text, f, ensure_ascii=False)
        
    # 3. Mixed
    mixed = {
        "source_video": {"video_id": "v-mixed", "file_name": "mixed.mp4", "file_path": "/tmp/mixed.mp4", "source_type": "local_file", "duration_ms": 10000, "language": "ja"},
        "transcript_segments": [
            {"segment_id": f"ts-{i}", "start_ms": i*1000, "end_ms": (i+1)*1000, "text": "音声とテキストの両方があります" * 5, "confidence": 0.9} for i in range(5)
        ],
        "ocr_segments": [
            {"ocr_id": f"ocr-{i}", "start_ms": i*1000, "end_ms": i*1000, "text": "画面上の文字も十分あります" * 5, "bbox": [0,0,10,10], "confidence": 0.9} for i in range(5)
        ]
    }
    with open(base_dir / "mixed.json", 'w', encoding='utf-8') as f: json.dump(mixed, f, ensure_ascii=False)
        
    # 4. Weak
    weak = {
        "source_video": {"video_id": "v-weak", "file_name": "weak.mp4", "file_path": "/tmp/weak.mp4", "source_type": "local_file", "duration_ms": 10000, "language": "ja"},
        "transcript_segments": [
            {"segment_id": "ts-1", "start_ms": 0, "end_ms": 1000, "text": "えーと", "confidence": 0.9}
        ],
        "ocr_segments": [
            {"ocr_id": "ocr-1", "start_ms": 0, "end_ms": 0, "text": "A", "bbox": [0,0,10,10], "confidence": 0.9}
        ]
    }
    with open(base_dir / "weak.json", 'w', encoding='utf-8') as f: json.dump(weak, f, ensure_ascii=False)

def run_tests():
    scenarios = ["speech", "text", "mixed", "weak"]
    for sc in scenarios:
        print(f"\n--- Testing Scenario: {sc} ---")
        input_file = f"samples/mock_evidences/{sc}.json"
        output_file = f"{sc}_spec.json"
        
        # Extract
        cmd_extract = f"python -m video_asset_manualize.build_asset extract {input_file} --output-dir samples/mock_evidences --output-name {output_file} --llm-provider dummy"
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        subprocess.run(cmd_extract, shell=True, env=env)
        
        # Validate (canonical should pass for all)
        spec_path = f"samples/mock_evidences/{output_file}"
        cmd_val_can = f"python -m video_asset_manualize.build_asset validate {spec_path} --level canonical"
        subprocess.run(cmd_val_can, shell=True, env=env)
        
        # Validate (acceptance should fail for weak, pass for others)
        cmd_val_acc = f"python -m video_asset_manualize.build_asset validate {spec_path} --level acceptance"
        env = os.environ.copy()
        env["PYTHONPATH"] = "src"
        res = subprocess.run(cmd_val_acc, shell=True, capture_output=True, text=True, env=env, encoding="utf-8")
        print("Acceptance Output:", res.stdout.strip())
        print("Acceptance Error:", res.stderr.strip())
        if sc == "weak":
            if res.returncode != 0 and "acceptance validation failed: evidence quality is 'weak'" in res.stdout:
                print(f"[OK] Weak evidence correctly rejected in acceptance")
            else:
                print(f"[FAIL] Weak evidence was not rejected properly")
        else:
            if res.returncode == 0:
                print(f"[OK] {sc} evidence correctly passed acceptance")
            else:
                print(f"[FAIL] {sc} evidence failed acceptance")

if __name__ == "__main__":
    create_mock_evidence()
    run_tests()
