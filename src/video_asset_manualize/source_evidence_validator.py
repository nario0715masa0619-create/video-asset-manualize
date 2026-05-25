"""
Source Evidence Validator - Validates source_evidence JSON against schema.
"""

import json
from pathlib import Path
from jsonschema import validate, ValidationError, Draft202012Validator

from .settings import settings


class SourceEvidenceValidator:
    """Validates source_evidence JSON against the official schema."""

    def __init__(self, schema_file: Path = None):
        """
        Initialize validator with source_evidence schema.

        Args:
            schema_file: Path to JSON Schema file.
        """
        self.schema_file = schema_file or (
            Path(settings.SCHEMAS_DIR) / "source_evidence.schema.json"
        )
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
        """Return the loaded schema."""
        return self._schema

    def validate(self, data: dict) -> bool:
        """
        Validate data against schema.

        Args:
            data: Dictionary to validate

        Returns:
            True if valid

        Raises:
            ValidationError: If validation fails
        """
        try:
            validate(instance=data, schema=self._schema)
            return True
        except ValidationError as e:
            raise ValidationError(
                f"Source evidence validation failed: {e.message}"
            ) from e

    def validate_file(self, file_path: Path) -> bool:
        """
        Load and validate a JSON file.

        Args:
            file_path: Path to JSON file

        Returns:
            True if valid
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        return self.validate(data)

    def get_validation_errors(self, data: dict) -> list:
        """
        Get all validation errors without raising exception.

        Args:
            data: Dictionary to validate

        Returns:
            List of error messages
        """
        errors = []
        validator = Draft202012Validator(self._schema)

        for error in sorted(validator.iter_errors(data), key=str):
            errors.append(str(error.message))

        return errors
