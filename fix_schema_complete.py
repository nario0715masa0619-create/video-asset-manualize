"""
training_asset_spec.schema.json を完全修正
すべての segment タイプで additionalProperties を削除
"""

from pathlib import Path
import json

schema_file = Path("schemas/training_asset_spec.schema.json")

with open(schema_file, "r", encoding="utf-8") as f:
    schema = json.load(f)

# すべての $defs セクション内の segment 定義を修正
if "$defs" in schema:
    for def_name in schema["$defs"]:
        obj = schema["$defs"][def_name]
        
        # additionalProperties が False なら削除
        if isinstance(obj, dict) and "additionalProperties" in obj:
            if obj["additionalProperties"] == False:
                del obj["additionalProperties"]
                print(f"✓ {def_name} から additionalProperties を削除")

# ファイルに保存
with open(schema_file, "w", encoding="utf-8") as f:
    json.dump(schema, f, indent=2, ensure_ascii=False)

print("\n✓ training_asset_spec.schema.json を完全修正しました")
