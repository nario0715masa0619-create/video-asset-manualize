"""
Canonical Acceptance Validator - Validates training_asset_spec at different levels
"""

from typing import Dict, Any, Tuple, List

class CanonicalAcceptanceValidator:
    """Validates training_asset_spec against AI-first canonical design criteria."""
    
    REQUIRED_METADATA = [
        'generated_at',
        'generation_mode',
        'provider',
        'model',
        'pipeline_version'
    ]
    
    @staticmethod
    def _create_result(is_valid: bool, level: str, errors: List[str], warnings: List[str]) -> Dict[str, Any]:
        return {
            "is_valid": is_valid,
            "level": level,
            "errors": errors,
            "warnings": warnings
        }

    @staticmethod
    def validate_basic(spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Level 1: Basic validation. 
        Checks if the spec is structurally sound and has essential top-level keys.
        """
        errors = []
        warnings = []
        
        required_keys = ['asset_meta', 'instructional_core']
        for key in required_keys:
            if key not in spec:
                errors.append(f"Missing required top-level key: {key}")
                
        if 'metadata' not in spec:
            warnings.append("Top-level 'metadata' block is missing (may be a legacy spec)")
            
        return CanonicalAcceptanceValidator._create_result(
            is_valid=len(errors) == 0,
            level="basic",
            errors=errors,
            warnings=warnings
        )

    @staticmethod
    def validate_canonical(spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Level 2: Canonical validation.
        Checks if the spec was generated via canonical mode with required metadata.
        """
        basic_res = CanonicalAcceptanceValidator.validate_basic(spec)
        errors = basic_res["errors"]
        warnings = basic_res["warnings"]
        
        metadata = spec.get('metadata', {})
        
        for field in CanonicalAcceptanceValidator.REQUIRED_METADATA:
            if field not in metadata:
                errors.append(f"Missing required metadata: {field}")
                
        mode = metadata.get('generation_mode')
        if mode != 'canonical':
            errors.append(f"generation_mode must be 'canonical', got '{mode}'")
            
        return CanonicalAcceptanceValidator._create_result(
            is_valid=len(errors) == 0,
            level="canonical",
            errors=errors,
            warnings=warnings
        )

    @staticmethod
    def validate_acceptance(spec: Dict[str, Any]) -> Dict[str, Any]:
        """
        Level 3: Acceptance validation.
        Checks semantic depth, instructional core structure, and traceability.
        """
        canonical_res = CanonicalAcceptanceValidator.validate_canonical(spec)
        errors = canonical_res["errors"]
        warnings = canonical_res["warnings"]
        
        core = spec.get('instructional_core', {})
        if not core:
            errors.append("instructional_core is empty")
        
        chapters = core.get('chapters', [])
        if not chapters:
            errors.append("instructional_core has no chapters")
            
        has_steps = False
        for chapter in chapters:
            for proc in chapter.get('procedures', []):
                if proc.get('steps'):
                    has_steps = True
                    break
        
        if not has_steps:
            errors.append("No actionable steps found in instructional_core")
            
        if 'source_evidence' not in spec:
            errors.append("source_evidence block is missing (required for traceability)")
            
        return CanonicalAcceptanceValidator._create_result(
            is_valid=len(errors) == 0,
            level="acceptance",
            errors=errors,
            warnings=warnings
        )
