'''
Compiled Training Asset Builder
'''

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime
from uuid import uuid4


class CompiledTrainingAsset:
    def __init__(self, project_id: str, title: str, description: str = ""):
        self.project_id = project_id
        self.title = title
        self.description = description
        self.assets = []
        self.created_at = datetime.utcnow().isoformat() + 'Z'
        self.compiled_id = f"compiled-{uuid4().hex[:8]}"
    
    def add_asset(self, spec: Dict[str, Any]):
        self.assets.append(spec)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            'compiled_id': self.compiled_id,
            'project_id': self.project_id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at,
            'asset_count': len(self.assets),
            'assets': self.assets
        }
    
    def get_table_of_contents(self) -> List[Dict[str, Any]]:
        toc = []
        for idx, asset in enumerate(self.assets, 1):
            asset_meta = asset.get('asset_meta', {})
            instructional_core = asset.get('instructional_core', {})
            chapters = instructional_core.get('chapters', [])
            
            toc.append({
                'section': idx,
                'asset_id': asset_meta.get('asset_id', 'unknown'),
                'title': asset_meta.get('title', 'Untitled'),
                'chapter_count': len(chapters),
                'chapters': [{'chapter_id': ch.get('chapter_id', ''), 'title': ch.get('title', '')} for ch in chapters]
            })
        return toc
    
    def save(self, output_path: str):
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)


class CompiledTrainingAssetBuilder:
    @staticmethod
    def compile_specs(specs: List[Dict[str, Any]], project_id: str, title: str, description: str = "") -> CompiledTrainingAsset:
        compiled = CompiledTrainingAsset(project_id, title, description)
        for spec in specs:
            compiled.add_asset(spec)
        return compiled
