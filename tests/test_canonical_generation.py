"""
Tests for Canonical Generation - Phase 12
"""
import pytest
import json
import os
from pathlib import Path
from typer.testing import CliRunner
from video_asset_manualize.build_asset import app
from video_asset_manualize.canonical_acceptance_validator import CanonicalAcceptanceValidator


@pytest.fixture
def clear_openai_api_key(monkeypatch):
    """Ensure OPENAI_API_KEY is not set during tests."""
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)


@pytest.fixture
def sample_source_evidence(tmp_path):
    """Create a valid sample source_evidence.json for testing."""
    evidence = {
        "source_video": {
            "video_id": "vid-001",
            "file_name": "test.mp4",
            "file_path": "/path/to/test.mp4",
            "source_type": "local_file",
            "duration_ms": 60000,
            "language": "en"
        },
        "transcript_segments": [
            {
                "segment_id": "ts-001",
                "start_ms": 0,
                "end_ms": 5000,
                "text": "This is a test video segment."
            }
        ],
        "ocr_segments": [],
        "screenshot_candidates": [],
        "speaker_segments": [],
        "evidence_links": []
    }
    
    evidence_file = tmp_path / "test_evidence.json"
    with open(evidence_file, 'w', encoding='utf-8') as f:
        json.dump(evidence, f, ensure_ascii=False)
    
    return str(evidence_file)


def test_extract_canonical_fails_without_key(sample_source_evidence, tmp_path, clear_openai_api_key):
    """Test that canonical generation fails without OPENAI_API_KEY."""
    runner = CliRunner()
    out_dir = str(tmp_path)
    result = runner.invoke(app, ["extract", sample_source_evidence, "--output-dir", out_dir, "--mode", "canonical"])
    
    assert result.exit_code == 1
    assert "OPENAI_API_KEY" in result.output or "canonical" in result.output.lower()


def test_extract_fallback_succeeds_without_key(sample_source_evidence, tmp_path, clear_openai_api_key):
    """Test that fallback generation succeeds even if OPENAI_API_KEY is missing."""
    runner = CliRunner()
    out_dir = str(tmp_path)
    result = runner.invoke(app, ["extract", sample_source_evidence, "--output-dir", out_dir, "--mode", "fallback"])
    
    assert result.exit_code == 0, f"Exit code: {result.exit_code}, Output: {result.output}"
    
    # Check that the output file was created
    output_file = Path(out_dir) / "extracted_spec.json"
    assert output_file.exists()
    
    # Verify metadata
    with open(output_file, encoding='utf-8') as f:
        spec = json.load(f)
    
    assert spec["metadata"]["generation_mode"] == "fallback"
    assert spec["metadata"]["provider"] == "non-llm"


def test_canonical_acceptance_validator_basic():
    """Test basic validation level."""
    spec = {
        "asset_meta": {"asset_id": "test-001"},
        "instructional_core": {}
    }
    
    result = CanonicalAcceptanceValidator.validate_basic(spec)
    assert result["is_valid"] == True
    assert result["level"] == "basic"


def test_canonical_acceptance_validator_canonical_fail():
    """Test canonical validation with fallback mode (should fail)."""
    spec = {
        "metadata": {"generation_mode": "fallback"},
        "asset_meta": {"asset_id": "test-001"},
        "instructional_core": {}
    }
    
    result = CanonicalAcceptanceValidator.validate_canonical(spec)
    assert result["is_valid"] == False
    assert any("canonical" in error.lower() for error in result["errors"])


def test_canonical_acceptance_validator_canonical_pass():
    """Test canonical validation with canonical mode (should pass)."""
    spec = {
        "metadata": {
            "generation_mode": "canonical",
            "generated_at": "2026-05-28T00:00:00Z",
            "provider": "openai",
            "model": "gpt-3.5-turbo",
            "pipeline_version": "12.0.0"
        },
        "asset_meta": {"asset_id": "test-001"},
        "instructional_core": {}
    }
    
    result = CanonicalAcceptanceValidator.validate_canonical(spec)
    assert result["is_valid"] == True
    assert result["level"] == "canonical"
