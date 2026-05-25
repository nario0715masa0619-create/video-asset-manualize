"""
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
