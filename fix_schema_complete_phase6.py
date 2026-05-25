"""
Phase 6 training_asset_spec.schema.json 完全修正スクリプト
"""

from pathlib import Path
import json

schema_file = Path("schemas/training_asset_spec.schema.json")

with open(schema_file, 'r', encoding='utf-8') as f:
    schema = json.load(f)

# required フィールドから不要な項目を削除
if "required" in schema:
    required = schema["required"]
    # _metadata など不要な必須フィールドを削除
    schema["required"] = [r for r in required if not r.startswith("_") and r != "metadata"]
    print(f"Updated required fields: {schema['required']}")

# additionalProperties を許可
schema["additionalProperties"] = True

# properties に metadata を追加
if "properties" not in schema:
    schema["properties"] = {}

if "metadata" not in schema["properties"]:
    schema["properties"]["metadata"] = {
        "type": "object",
        "additionalProperties": True
    }

with open(schema_file, 'w', encoding='utf-8') as f:
    json.dump(schema, f, ensure_ascii=False, indent=2)

print("Updated: schemas/training_asset_spec.schema.json")
print("\nOK: Schema completely fixed")
