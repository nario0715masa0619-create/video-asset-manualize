"""
Tests for Schema Alignment - Phase 12.3
"""
import pytest
import json
import os
from pathlib import Path
from jsonschema import validate, ValidationError

def load_schema(schema_name):
    schema_path = Path("schemas") / schema_name
    with open(schema_path, "r", encoding="utf-8") as f:
        return json.load(f)

@pytest.fixture
def training_asset_schema():
    return load_schema("training_asset_spec.schema.json")

def test_screenshot_candidate_field_alignment():
    """Verify screenshotCandidate uses timestamp_ms and image_path."""
    schema = load_schema("training_asset_spec.schema.json")
    screenshot_def = schema.get("$defs", {}).get("screenshotCandidate", {})
    
    assert "timestamp_ms" in screenshot_def.get("properties", {})
    assert "image_path" in screenshot_def.get("properties", {})
    
    assert "at_ms" not in screenshot_def.get("properties", {})
    assert "file_ref" not in screenshot_def.get("properties", {})

def test_speaker_segment_field_alignment():
    """Verify speakerSegment uses speaker_id."""
    schema = load_schema("training_asset_spec.schema.json")
    speaker_def = schema.get("$defs", {}).get("speakerSegment", {})
    
    assert "speaker_id" in speaker_def.get("properties", {})
    assert "speaker_segment_id" not in speaker_def.get("properties", {})

def test_evidence_link_field_alignment():
    """Verify evidenceLink uses link_id, target_id, etc."""
    schema = load_schema("training_asset_spec.schema.json")
    link_def = schema.get("$defs", {}).get("evidenceLink", {})
    
    assert "link_id" in link_def.get("properties", {})
    assert "target_id" in link_def.get("properties", {})
    
    assert "evidence_ref_id" not in link_def.get("properties", {})
    assert "related_step_id" not in link_def.get("properties", {})

def test_validate_spec_with_aligned_fields(training_asset_schema):
    """Test that a spec with aligned fields passes validation."""
    valid_spec = {
        "asset_meta": {
            "asset_id": "asset-001",
            "title": "Test Title"
        },
        "source_evidence": {
            "source_video": {
                "video_id": "vid-001",
                "file_name": "test.mp4",
                "file_path": "test.mp4",
                "source_type": "local_file",
                "duration_ms": 1000,
                "language": "ja"
            },
            "transcript_segments": [],
            "screenshot_candidates": [
                {
                    "screenshot_id": "sc-001",
                    "timestamp_ms": 500,
                    "image_path": "img.png"
                }
            ],
            "speaker_segments": [
                {
                    "speaker_id": "spk-001",
                    "start_ms": 0,
                    "end_ms": 1000
                }
            ],
            "evidence_links": [
                {
                    "link_id": "link-001",
                    "target_type": "step",
                    "target_id": "step-001",
                    "evidence_type": "screenshot_candidate",
                    "evidence_id": "sc-001"
                }
            ]
        },
        "instructional_core": {
            "chapters": [
                {
                    "chapter_id": "ch-001",
                    "title": "Test Chapter",
                    "procedures": [
                        {
                            "procedure_id": "proc-001",
                            "title": "Test Proc",
                            "steps": [
                                {
                                    "step_id": "step-001",
                                    "order": 1,
                                    "action": "Do something"
                                }
                            ]
                        }
                    ]
                }
            ]
        }
    }
    
    # This should pass without ValidationError
    validate(instance=valid_spec, schema=training_asset_schema)
