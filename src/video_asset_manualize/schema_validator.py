"""
JSON Schema validation for training_asset_spec.
"""

import json
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator

from .settings import settings


class SchemaValidator:
    """Validates training_asset_spec JSON against the official schema."""
    
    def __init__(self, schema_file: Path = None):
        self.schema_file = schema_file or settings.TRAINING_ASSET_SCHEMA_FILE
        self._schema = None
        self._load_schema()
    
    def _load_schema(self):
        """Load JSON Schema from file."""
        if not self.schema_file.exists():
            raise FileNotFoundError(f"Schema file not found: {self.schema_file}")
        
        with open(self.schema_file, "r", encoding="utf-8") as f:
            self._schema = json.load(f)
    
    @property
    def schema(self):
        return self._schema
    
    def validate(self, data: dict) -> bool:
        try:
            validate(instance=data, schema=self._schema)
            return True
        except ValidationError as e:
            raise ValidationError(f"Schema validation failed: {e.message}") from e
    
    def validate_file(self, file_path: Path) -> bool:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        return self.validate(data)
    
    def get_validation_errors(self, data: dict) -> list:
        errors = []
        validator = Draft202012Validator(self._schema)
        
        for error in sorted(validator.iter_errors(data), key=str):
            errors.append(str(error.message))
        
        return errors
