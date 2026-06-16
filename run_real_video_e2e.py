import os
import subprocess
from pathlib import Path

def run_e2e_tests():
    scenarios = ["speech", "text", "mixed", "weak"]
    base_out = Path("output/exports/real_tests")
    base_out.mkdir(parents=True, exist_ok=True)
    
    # We will use the proper providers for whisper and easyocr
    env = os.environ.copy()
    env["PYTHONPATH"] = "src"
    
    for sc in scenarios:
        print(f"\n======================================")
        print(f"Testing Scenario: {sc}")
        print(f"======================================")
        video_file = f"samples/real_test_videos/{sc}.mp4"
        evidence_file = base_out / f"{sc}_evidence.json"
        spec_file = base_out / f"{sc}_spec.json"
        
        # 1. Video extraction (using Whisper & EasyOCR)
        # We specify provider=whisper, ocr-provider=easyocr
        print(f"\n[Task 3] Running video extraction for {sc}...")
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
        print(f"[OK] video extraction completed for {sc}.")
        
        # 2. Canonical extract (using Dummy LLM to avoid real API calls & costs, but testing the pipeline)
        print(f"\n[Task 5] Running canonical extract for {sc}...")
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
        print(res_ext.stdout.strip().split("\n")[-1]) # print last line (success message)
        
        # 3. Validation
        print(f"\n[Task 6] Running validations for {sc}...")
        for lvl in ["basic", "canonical", "acceptance"]:
            cmd_val = f'python -m video_asset_manualize.build_asset validate {spec_file} --level {lvl}'
            res_val = subprocess.run(cmd_val, shell=True, env=env, text=True, capture_output=True, encoding="utf-8")
            if res_val.returncode == 0:
                print(f"  [OK] Validation {lvl} passed.")
            else:
                if lvl == "acceptance" and sc == "weak" and "acceptance validation failed: evidence quality is 'weak'" in res_val.stdout:
                    print(f"  [OK] Validation {lvl} correctly failed for weak evidence.")
                else:
                    print(f"  [FAIL] Validation {lvl} failed.")
                    print(res_val.stdout)
                    
        # 4. Build HTML/PDF
        if sc != "weak":
            print(f"\n[Task 7] Running build for {sc}...")
            cmd_build = f'python -m video_asset_manualize.build_asset build {spec_file} --output-dir {base_out}'
            res_build = subprocess.run(cmd_build, shell=True, env=env, text=True, capture_output=True, encoding="utf-8")
            if res_build.returncode == 0:
                print(f"[OK] Build passed for {sc}.")
            else:
                print(f"[FAIL] Build failed for {sc}.")
                print(res_build.stderr)

if __name__ == "__main__":
    run_e2e_tests()
