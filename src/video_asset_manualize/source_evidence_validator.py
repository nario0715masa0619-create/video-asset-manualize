"""
Source Evidence Validator - Validate source_evidence.json against schema
"""

import json
from pathlib import Path
import jsonschema


class SourceEvidenceValidator:
    """source_evidence.json をスキーマに対して検証"""
    
    def __init__(self):
        """初期化 - スキーマを読み込む"""
        schema_path = Path(__file__).parent.parent.parent / "schemas" / "source_evidence.schema.json"
        
        if not schema_path.exists():
            raise FileNotFoundError(f"Schema not found: {schema_path}")
        
        with open(schema_path, 'r', encoding='utf-8') as f:
            self.schema = json.load(f)
    
    def validate(self, data: dict) -> bool:
        """辞書型の source_evidence を検証"""
        try:
            jsonschema.validate(instance=data, schema=self.schema)
            return True
        except jsonschema.ValidationError as e:
            raise ValueError(f"Schema validation failed: {e.message}")
    
    def validate_file(self, file_path) -> bool:
        """JSON ファイルを検証"""
        file_path = str(file_path)
        file_path_obj = Path(file_path)
        
        if not file_path_obj.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        return self.validate(data)
    
    def get_validation_errors(self, data: dict) -> list:
        """検証エラーを取得"""
        validator = jsonschema.Draft7Validator(self.schema)
        errors = []
        for error in validator.iter_errors(data):
            errors.append({
                "path": list(error.absolute_path),
                "message": error.message
            })
        return errors
