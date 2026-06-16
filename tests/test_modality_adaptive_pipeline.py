import pytest
from typing import Dict, Any
from video_asset_manualize.modality_profile import ModalityProfile
from video_asset_manualize.ocr_temporal_aggregator import OCRTemporalAggregator
from video_asset_manualize.evidence_fusion import EvidenceFusion
from video_asset_manualize.canonical_acceptance_validator import CanonicalAcceptanceValidator

@pytest.fixture
def mock_speech_dominant_evidence() -> Dict[str, Any]:
    return {
        "source_video": {"video_id": "vid-001", "file_name": "test.mp4", "file_path": "/tmp/test.mp4", "source_type": "local_file", "duration_ms": 10000, "language": "ja"},
        "transcript_segments": [
            {"segment_id": "ts-1", "start_ms": 0, "end_ms": 2000, "text": "それでは始めます。", "confidence": 0.99},
            {"segment_id": "ts-2", "start_ms": 2500, "end_ms": 5000, "text": "ここでボタンを押してください。", "confidence": 0.99},
            {"segment_id": "ts-3", "start_ms": 6000, "end_ms": 9000, "text": "画面が切り替われば完了です。これは音声がメインの動画です。文字起こしの分量がOCRよりかなり多くなります。十分なテキスト量です。", "confidence": 0.99}
        ],
        "ocr_segments": []
    }

@pytest.fixture
def mock_text_dominant_evidence() -> Dict[str, Any]:
    # Make sure text > 50 chars to be strong
    text1 = "手順１：システムにログインする。ユーザーIDとパスワードを入力します。"
    text2 = "手順２：ダッシュボードから対象のプロジェクトを選択して、設定画面を開きます。"
    return {
        "source_video": {"video_id": "vid-002", "file_name": "test2.mp4", "file_path": "/tmp/test2.mp4", "source_type": "local_file", "duration_ms": 10000, "language": "ja"},
        "transcript_segments": [],
        "ocr_segments": [
            {"ocr_id": "ocr-1", "start_ms": 1000, "end_ms": 1000, "text": text1, "bbox": [0,0,10,10], "confidence": 0.9},
            {"ocr_id": "ocr-2", "start_ms": 1200, "end_ms": 1200, "text": text1, "bbox": [0,0,10,10], "confidence": 0.95},
            {"ocr_id": "ocr-3", "start_ms": 4000, "end_ms": 4000, "text": text2, "bbox": [0,0,10,10], "confidence": 0.9},
        ]
    }

@pytest.fixture
def mock_weak_evidence() -> Dict[str, Any]:
    return {
        "source_video": {"video_id": "vid-003", "file_name": "test3.mp4", "file_path": "/tmp/test3.mp4", "source_type": "local_file", "duration_ms": 10000, "language": "ja"},
        "transcript_segments": [
            {"segment_id": "ts-1", "start_ms": 0, "end_ms": 1000, "text": "はい", "confidence": 0.9}
        ],
        "ocr_segments": [
            {"ocr_id": "ocr-1", "start_ms": 0, "end_ms": 0, "text": "OK", "bbox": [0,0,10,10], "confidence": 0.9}
        ]
    }

def test_modality_profile_speech(mock_speech_dominant_evidence):
    profile = ModalityProfile.from_source_evidence(mock_speech_dominant_evidence)
    assert profile.dominant_modality == "speech_dominant"
    assert profile.evidence_quality in ["medium", "strong"]

def test_modality_profile_text(mock_text_dominant_evidence):
    profile = ModalityProfile.from_source_evidence(mock_text_dominant_evidence)
    assert profile.dominant_modality == "text_dominant"
    assert profile.evidence_quality in ["medium", "strong"]

def test_modality_profile_weak(mock_weak_evidence):
    profile = ModalityProfile.from_source_evidence(mock_weak_evidence)
    assert profile.dominant_modality == "weak_evidence"
    assert profile.evidence_quality == "weak"

def test_ocr_temporal_aggregator(mock_text_dominant_evidence):
    agg = OCRTemporalAggregator(gap_tolerance_ms=500)
    segments = agg.aggregate(mock_text_dominant_evidence["ocr_segments"])
    # 1000 and 1200 should be grouped
    assert len(segments) == 2
    assert segments[0]["start_ms"] == 1000
    assert segments[0]["end_ms"] == 1200
    assert segments[1]["start_ms"] == 4000

def test_evidence_fusion_text_dominant(mock_text_dominant_evidence):
    profile = ModalityProfile.from_source_evidence(mock_text_dominant_evidence)
    agg = OCRTemporalAggregator()
    visual_segs = agg.aggregate(mock_text_dominant_evidence["ocr_segments"])
    fusion = EvidenceFusion([], visual_segs, profile)
    fused_text = fusion.fuse_to_text()
    assert "ocr_primary" in fused_text
    assert "手順１" in fused_text

def test_acceptance_validation_blocks_weak():
    spec = {
        "asset_meta": {"asset_id": "1", "title": "test"},
        "source_evidence": {},
        "instructional_core": {
            "chapters": [{"chapter_id": "1", "title": "t", "procedures": [{"procedure_id": "1", "title": "t", "steps": [{"step_id": "1", "order": 1, "action": "test"}]}]}]
        },
        "metadata": {
            "generated_at": "2026",
            "generation_mode": "canonical",
            "provider": "openai",
            "model": "gpt-4",
            "pipeline_version": "0.1",
            "dominant_modality": "weak_evidence",
            "evidence_quality": "weak"
        }
    }
    validator = CanonicalAcceptanceValidator()
    res = validator.validate_acceptance(spec)
    assert not res["is_valid"]
    assert any("weak" in err for err in res["errors"])

def test_acceptance_validation_passes_strong():
    spec = {
        "asset_meta": {"asset_id": "1", "title": "test"},
        "source_evidence": {},
        "instructional_core": {
            "chapters": [{"chapter_id": "1", "title": "t", "procedures": [{"procedure_id": "1", "title": "t", "steps": [{"step_id": "1", "order": 1, "action": "test"}]}]}]
        },
        "metadata": {
            "generated_at": "2026",
            "generation_mode": "canonical",
            "provider": "openai",
            "model": "gpt-4",
            "pipeline_version": "0.1",
            "dominant_modality": "text_dominant",
            "evidence_quality": "strong"
        }
    }
    validator = CanonicalAcceptanceValidator()
    res = validator.validate_acceptance(spec)
    assert res["is_valid"]
