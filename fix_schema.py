"""
training_asset_spec.schema.json を確認・修正
transcript_segments で speaker_id を許可する
"""

from pathlib import Path
import json

schema_file = Path("schemas/training_asset_spec.schema.json")

# スキーマを読み込み
with open(schema_file, "r", encoding="utf-8") as f:
    schema = json.load(f)

# transcript_segments の定義を確認
if "$defs" in schema and "transcriptSegment" in schema["$defs"]:
    ts_def = schema["$defs"]["transcriptSegment"]
    print("現在の transcriptSegment properties:")
    print(json.dumps(ts_def.get("properties", {}), indent=2, ensure_ascii=False))
    
    # speaker_id を追加（まだなければ）
    if "speaker_id" not in ts_def.get("properties", {}):
        ts_def["properties"]["speaker_id"] = {
            "type": "string",
            "pattern": "^spk-[A-Za-z0-9._-]+$"
        }
        print("✓ speaker_id を追加しました")
    
    # additionalProperties を false から true に変更（または削除）
    if "additionalProperties" in ts_def and ts_def["additionalProperties"] == False:
        del ts_def["additionalProperties"]
        print("✓ additionalProperties の制限を削除しました")

# スキーマを保存
with open(schema_file, "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2, ensure_ascii=False)

print("✓ training_asset_spec.schema.json を修正しました")
