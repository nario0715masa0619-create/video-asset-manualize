"""
Generation Mode Definitions
"""
from enum import Enum
from typing import Any

class GenerationMode(str, Enum):
    """
    Generation mode definition for training_asset_spec
    """
    CANONICAL = "canonical"    # AI-based canonical generation (Production standard)
    FALLBACK = "fallback"      # Non-LLM fallback (Development/Emergency only)
    TEST = "test"              # Dummy mode (Testing only)
    UNKNOWN = "unknown"        # Non-canonical / Legacy specs without mode

def is_canonical(mode: Any) -> bool:
    """Check if the mode is CANONICAL."""
    try:
        return GenerationMode(mode) == GenerationMode.CANONICAL
    except ValueError:
        return False

def is_non_canonical(mode: Any) -> bool:
    """Check if the mode is non-canonical (fallback, test, unknown, or invalid)."""
    return not is_canonical(mode)

def normalize_generation_mode(value: Any) -> GenerationMode:
    """
    Safely convert a string value to GenerationMode enum.
    Returns GenerationMode.UNKNOWN if the value is invalid or missing.
    """
    if not value:
        return GenerationMode.UNKNOWN
    
    try:
        if isinstance(value, GenerationMode):
            return value
        return GenerationMode(str(value).lower())
    except ValueError:
        return GenerationMode.UNKNOWN
