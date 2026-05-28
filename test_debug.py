import sys
sys.path.insert(0, 'src')

from typer.testing import CliRunner
from video_asset_manualize.build_asset import app
import os
import json
from pathlib import Path

# OPENAI_API_KEY を削除
if 'OPENAI_API_KEY' in os.environ:
    del os.environ['OPENAI_API_KEY']

# テスト用の sample evidence を作成
sample_evidence = {
    "video_metadata": {"title": "Test Video"},
    "transcript_segments": [{"text": "hello world", "start_time": 0, "end_time": 1}],
    "ocr_segments": [],
    "frame_metadata": []
}

import tempfile
with tempfile.TemporaryDirectory() as tmpdir:
    evidence_path = Path(tmpdir) / "test_evidence.json"
    with open(evidence_path, 'w') as f:
        json.dump(sample_evidence, f)
    
    runner = CliRunner()
    result = runner.invoke(app, ["extract", str(evidence_path), "--mode", "fallback", "--output-dir", tmpdir])
    
    print("=== DEBUG OUTPUT ===")
    print("Exit Code:", result.exit_code)
    print("\n=== CLI Output ===")
    print(result.output)
    if result.exception:
        print("\n=== Exception ===")
        import traceback
        traceback.print_exception(type(result.exception), result.exception, result.exception.__traceback__)
