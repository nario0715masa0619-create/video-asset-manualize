"""
Build Training Asset Pipeline - MVP end-to-end pipeline.
"""

import json
from pathlib import Path
from datetime import datetime

from .schema_validator import SchemaValidator
from .training_asset_spec_builder import TrainingAssetSpecBuilder
from .html_manual_renderer import HTMLManualRenderer
from .pdf_manual_renderer import PDFManualRenderer


class BuildTrainingAssetPipeline:
    
    def __init__(self):
        self.validator = SchemaValidator()
        self.spec_builder = TrainingAssetSpecBuilder()
        self.html_renderer = HTMLManualRenderer()
        self.pdf_renderer = PDFManualRenderer()
        self.spec = None
        self.is_valid = False
    
    def load_spec(self, input_file: Path) -> bool:
        self.spec = self.spec_builder.load_from_file(input_file)
        try:
            self.validator.validate(self.spec)
            self.is_valid = True
            return True
        except Exception as e:
            print(f"Validation failed: {e}")
            return False
    
    def generate_html(self, output_file: Path) -> Path:
        if not self.spec:
            raise ValueError("No spec loaded")
        return self.html_renderer.render_to_file(self.spec, output_file)
    
    def generate_pdf(self, output_file: Path) -> Path:
        if not self.spec:
            raise ValueError("No spec loaded")
        return self.pdf_renderer.render_to_file(self.spec, output_file)
