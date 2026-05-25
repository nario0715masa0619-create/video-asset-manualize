"""
build_training_asset_pipeline.py を確認・修正
generate_outputs メソッドを追加
"""

from pathlib import Path

pipeline_file = Path("src/video_asset_manualize/build_training_asset_pipeline.py")

new_code = r'''"""
Build Training Asset Pipeline - Orchestrates the entire asset generation workflow.
"""

import json
from pathlib import Path

from .schema_validator import SchemaValidator
from .training_asset_spec_builder import TrainingAssetSpecBuilder
from .html_manual_renderer import HTMLManualRenderer
from .pdf_manual_renderer import PDFManualRenderer
from .settings import settings


class BuildTrainingAssetPipeline:
    """Orchestrates loading, validation, and rendering of training assets."""

    def __init__(self):
        """Initialize pipeline components."""
        self.validator = SchemaValidator()
        self.spec_builder = TrainingAssetSpecBuilder()
        self.html_renderer = HTMLManualRenderer()
        self.pdf_renderer = PDFManualRenderer()
        self.spec = None

    def load_spec(self, input_file: Path) -> dict:
        """
        Load training_asset_spec from file.

        Args:
            input_file: Path to JSON file

        Returns:
            Loaded spec dict
        """
        self.spec = self.spec_builder.load_from_file(input_file)
        return self.spec

    def validate(self) -> bool:
        """
        Validate loaded spec against schema.

        Returns:
            True if valid
        """
        if not self.spec:
            raise ValueError("No spec loaded")
        
        self.validator.validate(self.spec)
        return True

    def generate_html(self, output_file: Path = None) -> Path:
        """
        Generate HTML from spec.

        Args:
            output_file: Output path (default: asset-{id}_manual.html)

        Returns:
            Path to generated HTML
        """
        if not self.spec:
            raise ValueError("No spec loaded")

        if output_file is None:
            asset_id = self.spec.get("asset_meta", {}).get("asset_id", "unknown")
            output_file = settings.EXPORTS_DIR / f"{asset_id}_manual.html"

        output_file.parent.mkdir(parents=True, exist_ok=True)
        self.html_renderer.render_to_file(self.spec, output_file)
        return output_file

    def generate_pdf(self, output_file: Path = None) -> Path:
        """
        Generate PDF from spec.

        Args:
            output_file: Output path (default: asset-{id}_manual.pdf)

        Returns:
            Path to generated PDF
        """
        if not self.spec:
            raise ValueError("No spec loaded")

        if output_file is None:
            asset_id = self.spec.get("asset_meta", {}).get("asset_id", "unknown")
            output_file = settings.EXPORTS_DIR / f"{asset_id}_manual.pdf"

        output_file.parent.mkdir(parents=True, exist_ok=True)
        self.pdf_renderer.render_to_file(self.spec, output_file)
        return output_file

    def generate_outputs(
        self,
        input_file: Path,
        output_dir: Path = None,
        format: str = "all"
    ) -> dict:
        """
        Full pipeline: load → validate → render.

        Args:
            input_file: Path to training_asset_spec JSON
            output_dir: Output directory (default: settings.EXPORTS_DIR)
            format: Output format ("all", "html", "pdf", "json")

        Returns:
            Dict of generated file paths
        """
        if output_dir is None:
            output_dir = settings.EXPORTS_DIR

        output_dir.mkdir(parents=True, exist_ok=True)

        # Load and validate
        self.load_spec(Path(input_file))
        self.validate()

        outputs = {}

        # Generate HTML
        if format in ("all", "html"):
            html_file = output_dir / f"{self.spec.get('asset_meta', {}).get('asset_id', 'unknown')}_manual.html"
            self.generate_html(html_file)
            outputs["html"] = html_file

        # Generate PDF
        if format in ("all", "pdf"):
            pdf_file = output_dir / f"{self.spec.get('asset_meta', {}).get('asset_id', 'unknown')}_manual.pdf"
            self.generate_pdf(pdf_file)
            outputs["pdf"] = pdf_file

        # Save JSON spec
        if format in ("all", "json"):
            json_file = output_dir / f"{self.spec.get('asset_meta', {}).get('asset_id', 'unknown')}_spec.json"
            self.spec_builder.save_to_file(json_file)
            outputs["json"] = json_file

        return outputs
'''

with open(pipeline_file, "w", encoding="utf-8") as f:
    f.write(new_code)

print("✓ build_training_asset_pipeline.py を修正しました")
