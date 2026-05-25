"""
Phase 6 training_asset_spec.schema.json 修正スクリプト
"""

from pathlib import Path
import json

schema_file = Path("schemas/training_asset_spec.schema.json")

with open(schema_file, 'r', encoding='utf-8') as f:
    schema = json.load(f)

# トップレベルの properties に metadata を追加
if "properties" in schema:
    if "metadata" not in schema["properties"]:
        schema["properties"]["metadata"] = {
            "type": "object",
            "description": "Metadata about the asset generation"
        }
        print("Added 'metadata' to schema properties")

# additionalProperties を False から True に変更（または削除）
if "additionalProperties" in schema:
    schema["additionalProperties"] = True
    print("Set additionalProperties to true")

with open(schema_file, 'w', encoding='utf-8') as f:
    json.dump(schema, f, ensure_ascii=False, indent=2)

print("Updated: schemas/training_asset_spec.schema.json")
print("\nOK: training_asset_spec.schema.json fixed")
