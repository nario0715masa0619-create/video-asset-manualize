"""
source_evidence_to_training_asset_builder.py を修正
transcript_segments のフィールドをクリーンアップ
"""

from pathlib import Path

builder_file = Path("src/video_asset_manualize/source_evidence_to_training_asset_builder.py")

# ファイル読み込み
with open(builder_file, "r", encoding="utf-8") as f:
    content = f.read()

# _build_instructional_core メソッドの修正版を挿入
fix_code = '''
    def _build_instructional_core(self) -> dict:
        """Build instructional_core from transcript_segments."""
        transcripts = self.source_evidence.get("transcript_segments", [])

        if not transcripts:
            return {
                "summary": {
                    "purpose_summary": "transcript がありません"
                },
                "chapters": [{
                    "chapter_id": "chapter-001",
                    "title": "章1",
                    "procedures": [{
                        "procedure_id": "procedure-001",
                        "title": "手順1",
                        "steps": [{
                            "step_id": "step-001",
                            "order": 1,
                            "action": "transcript から自動抽出されていません"
                        }]
                    }]
                }],
                "global_cautions": ["自動抽出のため、内容を確認してください"]
            }

        # Simple extraction: group transcripts into chapters/procedures/steps
        steps = []
        for i, ts in enumerate(transcripts, 1):
            step = {
                "step_id": f"step-{i:03d}",
                "order": i,
                "action": ts.get("text", ""),
                "expected_result": "次のステップへ進む",
                "evidence_refs": [ts.get("segment_id", "")]
            }
            steps.append(step)

        return {
            "summary": {
                "purpose_summary": "video から自動抽出した手順",
                "outcome_summary": "各ステップに従って操作を実施"
            },
            "chapters": [{
                "chapter_id": "chapter-001",
                "title": "抽出された手順",
                "procedures": [{
                    "procedure_id": "procedure-001",
                    "title": "自動抽出手順",
                    "steps": steps
                }]
            }],
            "global_cautions": [
                "このデータは自動抽出です",
                "内容を確認し、必要に応じて修正してください"
            ]
        }
'''

# 古い _build_instructional_core を新しいバージョンで置き換え
import re
pattern = r'def _build_instructional_core\(self\) -> dict:.*?(?=\n    def |\n\n    def |$)'
content = re.sub(pattern, fix_code.strip(), content, flags=re.DOTALL)

# ファイル書き込み
with open(builder_file, "w", encoding="utf-8") as f:
    f.write(content)

print("✓ source_evidence_to_training_asset_builder.py を修正しました")
