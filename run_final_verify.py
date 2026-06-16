import os
import json
import subprocess
from pathlib import Path

def run_final_tests():
    scenarios = ["text", "mixed"]
    base_out = Path("output/exports/real_tests_final")
    base_out.mkdir(parents=True, exist_ok=True)
    
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    
    results = {}

    for sc in scenarios:
        print(f"\n======================================")
        print(f"Testing Scenario: {sc}")
        print(f"======================================")
        video_file = f"samples/real_test_videos/{sc}.mp4"
        evidence_file = base_out / f"{sc}_evidence.json"
        spec_file = base_out / f"{sc}_spec.json"
        
        results[sc] = {
            "video": "Fail", "extract": "Fail", "basic": "Fail", 
            "canonical": "Fail", "acceptance": "Fail", "build": "Fail",
            "modality": "unknown", "quality": "unknown"
        }
        
        print(f"[1] Running video extraction for {sc}...")
        cmd_video = (
            f'python -m video_asset_manualize.build_asset video {video_file} '
            f'--output-dir {base_out} --output-name {sc}_evidence.json '
            f'--provider whisper --ocr-provider easyocr --ocr-gpu'
        )
        res_vid = subprocess.run(cmd_video, shell=True, env=env, text=True, capture_output=True, encoding="utf-8")
        if res_vid.returncode != 0:
            print(f"[FAIL] video extraction failed for {sc}:")
            print(res_vid.stderr)
            continue
        results[sc]["video"] = "Pass"
        
        print(f"[2] Running canonical extract for {sc}...")
        cmd_extract = (
            f'python -m video_asset_manualize.build_asset extract {evidence_file} '
            f'--output-dir {base_out} --output-name {sc}_spec.json '
            f'--mode canonical --llm-provider dummy'
        )
        res_ext = subprocess.run(cmd_extract, shell=True, env=env, text=True, capture_output=True, encoding="utf-8")
        if res_ext.returncode != 0:
            print(f"[FAIL] extract failed for {sc}:")
            print(res_ext.stderr)
            continue
        results[sc]["extract"] = "Pass"
        
        # Read the spec file to get modality info
        try:
            with open(spec_file, 'r', encoding='utf-8') as f:
                spec_data = json.load(f)
                metadata = spec_data.get('metadata', {})
                results[sc]["modality"] = metadata.get('dominant_modality', 'unknown')
                results[sc]["quality"] = metadata.get('evidence_quality', 'unknown')
        except Exception as e:
            print("Failed to read spec file for metadata:", e)
        
        print(f"[3] Running validations for {sc}...")
        for lvl in ["basic", "canonical", "acceptance"]:
            cmd_val = f'python -m video_asset_manualize.build_asset validate {spec_file} --level {lvl}'
            res_val = subprocess.run(cmd_val, shell=True, env=env, text=True, capture_output=True, encoding="utf-8")
            if res_val.returncode == 0:
                results[sc][lvl] = "Pass"
            else:
                print(f"[FAIL] {lvl} validation failed.")
                print(res_val.stdout)
                
        print(f"[4] Running build for {sc}...")
        cmd_build = f'python -m video_asset_manualize.build_asset build {spec_file} --output-dir {base_out}'
        res_build = subprocess.run(cmd_build, shell=True, env=env, text=True, capture_output=True, encoding="utf-8")
        if res_build.returncode == 0:
            results[sc]["build"] = "Pass"
        else:
            print(f"[FAIL] build failed.")
            print(res_build.stderr)
            
    print("\n\nFINAL REPORT DATA:")
    print(json.dumps(results, indent=2))

if __name__ == "__main__":
    run_final_tests()
