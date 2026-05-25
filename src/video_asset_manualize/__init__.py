"""
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
