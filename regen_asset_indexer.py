"""
asset_indexer 完全再生成
"""

from pathlib import Path

asset_indexer_code = """'''
Asset Indexer - 生成済み成果物のインデックス作成
'''

import json
from pathlib import Path
from typing import List, Dict, Any


class AssetIndexer:
    def __init__(self, exports_dir: str = "output/exports"):
        self.exports_dir = Path(exports_dir)
    
    def scan_assets(self) -> List[Dict[str, Any]]:
        assets_by_id = {}
        
        if not self.exports_dir.exists():
            return []
        
        for spec_file in sorted(self.exports_dir.glob("*_spec.json")):
            if "_compiled" in spec_file.name or "_booklet" in spec_file.name:
                continue
            
            try:
                with open(spec_file, 'r', encoding='utf-8') as f:
                    spec = json.load(f)
                
                asset_meta = spec.get('asset_meta', {})
                asset_id = asset_meta.get('asset_id', '')
                
                if asset_id and asset_id not in assets_by_id:
                    assets_by_id[asset_id] = {
                        'asset_id': asset_id,
                        'title': asset_meta.get('title', 'Untitled'),
                        'language': asset_meta.get('language', 'unknown'),
                        'status': asset_meta.get('status', 'draft'),
                        'created_at': asset_meta.get('created_at', ''),
                        'spec_file': str(spec_file),
                        'html_file': str(self.exports_dir / f"{asset_id}_manual.html"),
                        'pdf_file': str(self.exports_dir / f"{asset_id}_manual.pdf"),
                    }
            except Exception as e:
                pass
        
        return sorted(list(assets_by_id.values()), key=lambda x: x.get('created_at', ''), reverse=True)
    
    def scan_booklets(self) -> List[Dict[str, Any]]:
        booklets_by_id = {}
        
        if not self.exports_dir.exists():
            return []
        
        for compiled_file in sorted(self.exports_dir.glob("*_compiled.json")):
            try:
                with open(compiled_file, 'r', encoding='utf-8') as f:
                    compiled = json.load(f)
                
                project_id = compiled.get('project_id', '')
                
                if project_id and project_id not in booklets_by_id:
                    booklets_by_id[project_id] = {
                        'project_id': project_id,
                        'title': compiled.get('title', 'Untitled'),
                        'asset_count': compiled.get('asset_count', 0),
                        'created_at': compiled.get('created_at', ''),
                        'compiled_file': str(compiled_file),
                        'html_file': str(self.exports_dir / f"{project_id}_booklet.html"),
                        'pdf_file': str(self.exports_dir / f"{project_id}_booklet.pdf"),
                    }
            except Exception as e:
                pass
        
        return sorted(list(booklets_by_id.values()), key=lambda x: x.get('created_at', ''), reverse=True)
"""

Path("src/video_asset_manualize/asset_indexer.py").write_text(asset_indexer_code, encoding='utf-8')
print("OK: asset_indexer.py completely regenerated")
