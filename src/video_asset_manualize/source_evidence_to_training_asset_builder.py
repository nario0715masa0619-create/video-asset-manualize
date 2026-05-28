"""
Source Evidence to Training Asset Builder - Converts source_evidence to training_asset_spec.
"""

import json
from pathlib import Path
from datetime import datetime
from uuid import uuid4

from .training_asset_spec_builder import TrainingAssetSpecBuilder


class SourceEvidenceToTrainingAssetBuilder:
    """
    MVP Builder: Converts source_evidence into training_asset_spec.
    Extracts key information from transcript and structures it into chapters/procedures/steps.
    """

    def __init__(self):
        """Initialize builder."""
        self.source_evidence = None
        self.spec_builder = TrainingAssetSpecBuilder()

    def load_source_evidence(self, file_path: Path) -> dict:
        """
        Load source_evidence from file.

        Args:
            file_path: Path to source_evidence JSON

        Returns:
            Loaded source_evidence
        """
        if not file_path.exists():
            raise FileNotFoundError(f"File not found: {file_path}")

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        self.source_evidence = data
        return self.source_evidence

    def build_training_asset_spec(self, asset_meta: dict = None) -> dict:
        """
        Build training_asset_spec from source_evidence.

        Args:
            asset_meta: Optional metadata overrides

        Returns:
            Generated training_asset_spec
        """
        if not self.source_evidence:
            raise ValueError("No source_evidence loaded")

        # Asset metadata
        if not asset_meta:
            asset_meta = self._build_asset_meta()

        # Source evidence section (minimal - just pass through)
        source_evidence = {}

        # Instructional core (extracted from transcripts)
        instructional_core = self._build_instructional_core()

        # Derived views (basic generation)
        derived_views = self._build_derived_views()

        # Metadata
        metadata = {
            "schema_version": "0.1.0",
            "generated_at": datetime.now().isoformat(),
            "pipeline_version": "0.2.0",
            "generation_context": {
                "mode": "source_evidence_extraction",
                "source": "phase2_extraction"
            },
            "review_status": "unreviewed",
            "review_notes": ["自動抽出のため、レビューが必要です"]
        }

        # Build complete spec
        spec = {
            "asset_meta": asset_meta,
            "instructional_core": instructional_core,
            "derived_views": derived_views,
            "metadata": metadata
        }

        # Store in builder
        self.spec_builder.spec = spec

        return spec

    def build_from_file(self, file_path: str) -> dict:
        """Convenience method to load and build in one step."""
        self.load_source_evidence(Path(file_path))
        return self.build_training_asset_spec()

    def _build_asset_meta(self) -> dict:
        """Build asset_meta from source_evidence."""
        source_video = self.source_evidence.get("source_video", {})

        return {
            "asset_id": f"asset-{uuid4().hex[:8]}",
            "source_video_id": source_video.get("video_id", "unknown"),
            "title": f"{source_video.get('file_name', '動画')}からの自動抽出",
            "purpose": "動画から自動抽出した手順",
            "target_audience": ["全員"],
            "target_department": [],
            "prerequisites": [],
            "language": "ja-JP",
            "status": "draft",
            "version": "0.1.0",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }

    def _build_instructional_core(self) -> dict:
        """Build instructional_core from transcript_segments."""
        transcripts = self.source_evidence.get("transcript_segments", [])

        if not transcripts:
            return {
                "summary": {
                    "purpose_summary": "transcript がありません"
                },
                "chapters": [{
                    "chapter_id": "chapter-001",
                    "title": "章1",
                    "procedures": [{
                        "procedure_id": "procedure-001",
                        "title": "手順1",
                        "steps": [{
                            "step_id": "step-001",
                            "order": 1,
                            "action": "transcript から自動抽出されていません"
                        }]
                    }]
                }],
                "global_cautions": ["自動抽出のため、内容を確認してください"]
            }

        # Simple extraction: group transcripts into chapters/procedures/steps
        steps = []
        for i, ts in enumerate(transcripts, 1):
            step = {
                "step_id": f"step-{i:03d}",
                "order": i,
                "action": ts.get("text", ""),
                "expected_result": "次のステップへ進む"
            }
            steps.append(step)

        return {
            "summary": {
                "purpose_summary": "video から自動抽出した手順",
                "outcome_summary": "各ステップに従って操作を実施"
            },
            "chapters": [{
                "chapter_id": "chapter-001",
                "title": "抽出された手順",
                "procedures": [{
                    "procedure_id": "procedure-001",
                    "title": "自動抽出手順",
                    "steps": steps
                }]
            }],
            "global_cautions": [
                "このデータは自動抽出です",
                "内容を確認し、必要に応じて修正してください"
            ]
        }

    def _build_derived_views(self) -> dict:
        """Build derived_views (minimal)."""
        return {
            "beginner_view": {
                "title": "新人向け簡易版",
                "key_points": ["自動抽出のため、確認が必要です"]
            }
        }

    def save_training_asset_spec(self, output_file: Path) -> Path:
        """
        Save generated training_asset_spec to file.

        Args:
            output_file: Path to save

        Returns:
            Path to saved file
        """
        return self.spec_builder.save_to_file(output_file)
