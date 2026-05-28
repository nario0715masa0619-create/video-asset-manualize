"""
Orchestration Layer - Handles generation modes, providers, and metadata
"""

from typing import Dict, Any
from datetime import datetime, timezone as tz

from .generation_mode import GenerationMode, normalize_generation_mode
from .provider_factory import ProviderFactory
from .llm_training_asset_builder import LLMTrainingAssetBuilder
from .source_evidence_to_training_asset_builder import SourceEvidenceToTrainingAssetBuilder


class Orchestrator:
    """Orchestrates the asset generation pipeline based on AI-first canonical design."""

    @staticmethod
    def resolve_generation_mode(mode_str: str) -> GenerationMode:
        """Resolve string mode to GenerationMode enum."""
        mode = normalize_generation_mode(mode_str)
        if mode == GenerationMode.UNKNOWN:
            raise ValueError(f"Invalid generation mode: {mode_str}")
        return mode

    @staticmethod
    def apply_generation_metadata(
        spec: Dict[str, Any],
        mode: GenerationMode,
        provider_name: str,
        model_name: str
    ) -> None:
        """Apply top-level metadata required for AI-first canonical design."""
        now = datetime.now(tz.utc).isoformat()

        if "metadata" not in spec:
            spec["metadata"] = {}

        spec["metadata"].update({
            "generated_at": now,
            "generation_mode": mode.value,
            "provider": provider_name,
            "model": model_name,
            "pipeline_version": "12.0.0"
        })

    @staticmethod
    def extract_with_mode(
        source_evidence_path: str,
        mode: GenerationMode,
        llm_provider_name: str = "openai"
    ) -> Dict[str, Any]:
        """
        Execute the extraction pipeline based on the specified generation mode.
        """
        if mode == GenerationMode.CANONICAL:
            # Canonical requires LLM provider
            provider = ProviderFactory.create_llm_provider(provider_type=llm_provider_name)
            builder = LLMTrainingAssetBuilder(llm_provider=provider)
            spec = builder.build_from_file(source_evidence_path)

            # The provider should expose its model name, default to unknown
            model_name = getattr(provider, 'model', 'unknown')

            Orchestrator.apply_generation_metadata(spec, mode, llm_provider_name, model_name)
            return spec

        elif mode in (GenerationMode.FALLBACK, GenerationMode.TEST):
            # Fallback/Test uses non-LLM builder
            builder = SourceEvidenceToTrainingAssetBuilder()
            spec = builder.build_from_file(source_evidence_path)

            Orchestrator.apply_generation_metadata(spec, mode, "non-llm", "n/a")
            return spec

        else:
            raise ValueError(f"Unsupported extraction mode: {mode.value}")
