"""
VideoAsset Manualize MVP - 自動ファイル生成スクリプト
"""

import json
from pathlib import Path
from datetime import datetime

files_to_create = {}

files_to_create['src/video_asset_manualize/__init__.py'] = '''"""
VideoAsset Manualize - Convert training videos to structured educational assets.
"""

__version__ = "0.1.0"
__author__ = "nario0715masa0619-create"

from .settings import settings
from .schema_validator import SchemaValidator
from .training_asset_spec_builder import TrainingAssetSpecBuilder
from .html_manual_renderer import HTMLManualRenderer
from .pdf_manual_renderer import PDFManualRenderer
from .build_training_asset_pipeline import BuildTrainingAssetPipeline

__all__ = [
    "settings",
    "SchemaValidator",
    "TrainingAssetSpecBuilder",
    "HTMLManualRenderer",
    "PDFManualRenderer",
    "BuildTrainingAssetPipeline",
]
'''

files_to_create['src/video_asset_manualize/settings.py'] = '''"""
Configuration and settings management for VideoAsset Manualize.
"""

import os
from pathlib import Path
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Application settings loaded from environment variables or .env file.
    """
    
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent
    SRC_DIR: Path = PROJECT_ROOT / "src"
    SAMPLES_DIR: Path = PROJECT_ROOT / "samples"
    SCHEMAS_DIR: Path = PROJECT_ROOT / "schemas"
    OUTPUT_DIR: Path = PROJECT_ROOT / "output"
    EXPORTS_DIR: Path = OUTPUT_DIR / "exports"
    
    SCHEMA_VERSION: str = "0.1.0"
    TRAINING_ASSET_SCHEMA_FILE: Path = SCHEMAS_DIR / "training_asset_spec.schema.json"
    
    TEMPLATES_DIR: Path = SRC_DIR / "video_asset_manualize" / "templates"
    HTML_TEMPLATE_FILE: Path = TEMPLATES_DIR / "manual_template.html"
    
    LOG_LEVEL: str = "INFO"
    
    ENABLE_SCHEMA_VALIDATION: bool = True
    ENABLE_HTML_GENERATION: bool = True
    ENABLE_PDF_GENERATION: bool = True
    
    PDF_PAPER_SIZE: str = "A4"
    PDF_MARGIN_TOP: int = 20
    PDF_MARGIN_BOTTOM: int = 20
    PDF_MARGIN_LEFT: int = 20
    PDF_MARGIN_RIGHT: int = 20
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        case_sensitive = True
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
        self.EXPORTS_DIR.mkdir(parents=True, exist_ok=True)


settings = Settings()
'''

files_to_create['src/video_asset_manualize/__main__.py'] = '''"""
CLI entry point for VideoAsset Manualize.
"""

from .build_asset import app

if __name__ == "__main__":
    app()
'''

files_to_create['src/video_asset_manualize/schema_validator.py'] = '''"""
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
'''

files_to_create['src/video_asset_manualize/training_asset_spec_builder.py'] = '''"""
Training Asset Spec Builder - MVP minimal builder (loads existing JSON).
"""

import json
from pathlib import Path
from datetime import datetime


class TrainingAssetSpecBuilder:
    """
    MVP Builder: For now, this primarily loads and validates existing JSON specs.
    Future versions will build specs from raw video data.
    """
    
    def __init__(self):
        self.spec = None
    
    def load_from_file(self, file_path: Path) -> dict:
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")
        
        with open(file_path, "r", encoding="utf-8") as f:
            self.spec = json.load(f)
        
        return self.spec
    
    def load_from_dict(self, spec_dict: dict) -> dict:
        self.spec = spec_dict
        return self.spec
    
    def get_spec(self) -> dict:
        return self.spec
    
    def update_metadata(self, **kwargs) -> dict:
        if not self.spec:
            raise ValueError("No spec loaded. Load or create a spec first.")
        
        if "_metadata" not in self.spec:
            self.spec["_metadata"] = {}
        
        self.spec["_metadata"].update(kwargs)
        return self.spec
    
    def update_generated_at(self) -> dict:
        if not self.spec:
            raise ValueError("No spec loaded")
        
        if "_metadata" not in self.spec:
            self.spec["_metadata"] = {}
        
        self.spec["_metadata"]["generated_at"] = datetime.now().isoformat()
        return self.spec
    
    def save_to_file(self, output_file: Path) -> Path:
        if not self.spec:
            raise ValueError("No spec loaded")
        
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(self.spec, f, ensure_ascii=False, indent=2)
        
        return output_file
'''

files_to_create['src/video_asset_manualize/html_manual_renderer.py'] = '''"""
HTML Manual Renderer - Renders training_asset_spec to HTML.
"""

import json
from pathlib import Path
from datetime import datetime
from jinja2 import Template

from .settings import settings


class HTMLManualRenderer:
    """Renders training_asset_spec JSON to HTML manual."""
    
    DEFAULT_TEMPLATE = """<!DOCTYPE html>
<html lang="ja">
<head>
    <meta charset="UTF-8">
    <title>{{ asset_meta.title }}</title>
    <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; color: #333; background: #f5f5f5; padding: 20px; }
        .container { max-width: 900px; margin: 0 auto; background: white; padding: 40px; border-radius: 8px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); }
        h1 { color: #000; border-bottom: 3px solid #007bff; padding-bottom: 10px; }
        h2 { color: #007bff; border-left: 4px solid #007bff; padding-left: 10px; margin-top: 30px; }
        h3 { color: #333; margin-top: 20px; }
        .step { margin: 15px 0; padding: 10px; background: #f0f8ff; border-left: 3px solid #007bff; }
        .caution { background: #fff3cd; border: 1px solid #ffc107; padding: 10px; margin: 10px 0; }
        code { background: #f4f4f4; padding: 2px 6px; border-radius: 3px; }
        .metadata { font-size: 12px; color: #666; margin: 10px 0; }
        footer { margin-top: 40px; padding-top: 20px; border-top: 1px solid #ccc; font-size: 11px; color: #999; }
    </style>
</head>
<body>
    <div class="container">
        <h1>{{ asset_meta.title }}</h1>
        <div class="metadata">
            <div><strong>目的:</strong> {{ asset_meta.purpose or 'N/A' }}</div>
            <div><strong>対象者:</strong> {{ asset_meta.target_audience | join(', ') or 'N/A' }}</div>
            <div><strong>ステータス:</strong> {{ asset_meta.status }}</div>
        </div>
        
        {% if asset_meta.prerequisites %}
        <h2>前提条件</h2>
        <ul>
        {% for pre in asset_meta.prerequisites %}
            <li>{{ pre }}</li>
        {% endfor %}
        </ul>
        {% endif %}
        
        {% if instructional_core.global_cautions %}
        <div class="caution">
            <strong>⚠️ 注意事項</strong>
            <ul>
            {% for caution in instructional_core.global_cautions %}
                <li>{{ caution }}</li>
            {% endfor %}
            </ul>
        </div>
        {% endif %}
        
        {% for chapter in instructional_core.chapters %}
        <h2>{{ chapter.title }}</h2>
        {% for procedure in chapter.procedures %}
            <h3>{{ procedure.title }}</h3>
            {% for step in procedure.steps %}
            <div class="step">
                <strong>ステップ {{ step.order }}:</strong> {{ step.action }}
                {% if step.expected_result %}<div><em>期待: {{ step.expected_result }}</em></div>{% endif %}
            </div>
            {% endfor %}
        {% endfor %}
        {% endfor %}
        
        <footer>
            <p>Generated on {{ _metadata.generated_at }} (Schema v{{ _metadata.schema_version }})</p>
        </footer>
    </div>
</body>
</html>"""
    
    def __init__(self):
        self.template = Template(self.DEFAULT_TEMPLATE)
    
    def render(self, asset_spec: dict) -> str:
        html = self.template.render(
            asset_meta=asset_spec.get("asset_meta", {}),
            instructional_core=asset_spec.get("instructional_core", {}),
            _metadata=asset_spec.get("_metadata", {}),
        )
        return html
    
    def render_to_file(self, asset_spec: dict, output_file: Path) -> Path:
        html = self.render(asset_spec)
        output_file.parent.mkdir(parents=True, exist_ok=True)
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(html)
        return output_file
'''

files_to_create['src/video_asset_manualize/pdf_manual_renderer.py'] = '''"""
PDF Manual Renderer - Renders training_asset_spec to PDF.
"""

import json
from pathlib import Path
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.lib import colors

from .settings import settings


class PDFManualRenderer:
    """Renders training_asset_spec JSON to PDF manual."""
    
    def __init__(self):
        self.styles = getSampleStyleSheet()
        self._setup_custom_styles()
    
    def _setup_custom_styles(self):
        self.styles.add(ParagraphStyle(
            name='CustomTitle',
            parent=self.styles['Heading1'],
            fontSize=24,
            textColor=colors.HexColor('#000000'),
            spaceAfter=12,
        ))
        self.styles.add(ParagraphStyle(
            name='CustomHeading2',
            parent=self.styles['Heading2'],
            fontSize=16,
            textColor=colors.HexColor('#007bff'),
            spaceAfter=12,
        ))
    
    def _build_document(self, asset_spec: dict) -> list:
        story = []
        asset_meta = asset_spec.get('asset_meta', {})
        instructional_core = asset_spec.get('instructional_core', {})
        _metadata = asset_spec.get('_metadata', {})
        
        story.append(Paragraph(asset_meta.get('title', 'Manual'), self.styles['CustomTitle']))
        story.append(Spacer(1, 12*mm))
        
        meta = f"<b>目的:</b> {asset_meta.get('purpose', 'N/A')}<br/><b>対象者:</b> {', '.join(asset_meta.get('target_audience', []))}"
        story.append(Paragraph(meta, self.styles['Normal']))
        story.append(Spacer(1, 12*mm))
        
        for chapter in instructional_core.get('chapters', []):
            story.append(PageBreak())
            story.append(Paragraph(chapter.get('title', ''), self.styles['CustomHeading2']))
            
            for procedure in chapter.get('procedures', []):
                story.append(Paragraph(procedure.get('title', ''), self.styles['Heading3']))
                
                for step in procedure.get('steps', []):
                    text = f"<b>ステップ {step.get('order')}:</b> {step.get('action', '')}"
                    story.append(Paragraph(text, self.styles['Normal']))
                
                story.append(Spacer(1, 6*mm))
        
        story.append(Spacer(1, 12*mm))
        story.append(Paragraph(f"<i>Generated on {_metadata.get('generated_at', 'N/A')}</i>", self.styles['Normal']))
        
        return story
    
    def render_to_file(self, asset_spec: dict, output_file: Path) -> Path:
        output_file.parent.mkdir(parents=True, exist_ok=True)
        
        doc = SimpleDocTemplate(
            str(output_file),
            pagesize=A4,
            rightMargin=20*mm,
            leftMargin=20*mm,
            topMargin=20*mm,
            bottomMargin=20*mm,
        )
        
        story = self._build_document(asset_spec)
        doc.build(story)
        
        return output_file
'''

files_to_create['src/video_asset_manualize/build_training_asset_pipeline.py'] = '''"""
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
'''

files_to_create['src/video_asset_manualize/build_asset.py'] = '''"""
CLI Interface for building training assets.
"""

import json
from pathlib import Path
import typer
from rich.console import Console

from .build_training_asset_pipeline import BuildTrainingAssetPipeline
from .settings import settings

app = typer.Typer(help="VideoAsset Manualize - Convert training videos to structured assets")
console = Console()


@app.command()
def build(
    input_file: Path = typer.Argument(..., help="Path to input training_asset_spec.json"),
    output_dir: Path = typer.Option(settings.EXPORTS_DIR, "--output", "-o", help="Output directory"),
):
    """Build training assets from JSON specification."""
    
    if not input_file.exists():
        console.print(f"[red]Error: Input file not found: {input_file}[/red]")
        raise typer.Exit(code=1)
    
    pipeline = BuildTrainingAssetPipeline()
    
    try:
        console.print(f"[cyan]Loading: {input_file}[/cyan]")
        if not pipeline.load_spec(input_file):
            console.print("[yellow]Warning: Validation failed but continuing[/yellow]")
        else:
            console.print("[green]✓ Validation passed[/green]")
        
        console.print(f"[cyan]Generating outputs to: {output_dir}[/cyan]")
        output_dir.mkdir(parents=True, exist_ok=True)
        
        asset_id = pipeline.spec.get("asset_meta", {}).get("asset_id", "asset")
        
        html_file = output_dir / f"{asset_id}_manual.html"
        pipeline.generate_html(html_file)
        console.print(f"[green]✓[/green] Generated HTML: {html_file}")
        
        pdf_file = output_dir / f"{asset_id}_manual.pdf"
        pipeline.generate_pdf(pdf_file)
        console.print(f"[green]✓[/green] Generated PDF: {pdf_file}")
        
        console.print(f"[green bold]\\n✓ Build completed successfully![/green bold]")
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        raise typer.Exit(code=1)


@app.command()
def validate(input_file: Path = typer.Argument(..., help="Path to training_asset_spec.json")):
    """Validate JSON against schema."""
    
    if not input_file.exists():
        console.print(f"[red]Error: File not found: {input_file}[/red]")
        raise typer.Exit(code=1)
    
    pipeline = BuildTrainingAssetPipeline()
    
    try:
        console.print(f"[cyan]Validating: {input_file}[/cyan]")
        with open(input_file, "r", encoding="utf-8") as f:
            data = json.load(f)
        
        pipeline.validator.validate(data)
        console.print("[green bold]✓ Validation passed![/green bold]")
        
    except Exception as e:
        console.print(f"[red]Validation Error: {e}[/red]")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()
'''

files_to_create['main.py'] = '''"""
Main entry point for VideoAsset Manualize MVP.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from video_asset_manualize.build_asset import app

if __name__ == "__main__":
    app()
'''

def create_files():
    total = len(files_to_create)
    created = 0
    
    print("\n" + "="*70)
    print("VideoAsset Manualize MVP - ファイル自動生成")
    print("="*70 + "\n")
    
    for file_path, content in files_to_create.items():
        file_obj = Path(file_path)
        file_obj.parent.mkdir(parents=True, exist_ok=True)
        
        try:
            with open(file_obj, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"✓ Created: {file_path}")
            created += 1
        except Exception as e:
            print(f"✗ Error: {file_path} - {e}")
    
    print(f"\n{created}/{total} ファイルを生成しました。")
    print("\n" + "="*70)
    print("次のステップ:")
    print("="*70)
    print("\n1. 依存関係をインストール:")
    print("   pip install -r requirements.txt\n")
    print("2. スキーマ検証:")
    print("   python -m video_asset_manualize.build_asset validate samples/sample_training_asset_spec.json\n")
    print("3. 完全ビルド:")
    print("   python -m video_asset_manualize.build_asset build samples/sample_training_asset_spec.json\n")
    print("="*70 + "\n")


if __name__ == '__main__':
    create_files()
