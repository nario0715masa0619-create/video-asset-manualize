"""
Phase 8 asset_indexer 重複排除修正スクリプト
"""

from pathlib import Path

asset_indexer_code = """'''
Asset Indexer - 生成済み成果物のインデックス作成
'''

import json
from pathlib import Path
from typing import List, Dict, Any
from datetime import datetime


class AssetIndexer:
    '''生成済み成果物をスキャンしてインデックス作成'''
    
    def __init__(self, exports_dir: str = "output/exports"):
        self.exports_dir = Path(exports_dir)
    
    def scan_assets(self) -> List[Dict[str, Any]]:
        '''成果物をスキャンしてリスト化（重複排除）'''
        assets_dict = {}
        
        if not self.exports_dir.exists():
            return []
        
        # _spec.json ファイルを探す
        for spec_file in self.exports_dir.glob("*_spec.json"):
            try:
                with open(spec_file, 'r', encoding='utf-8') as f:
                    spec = json.load(f)
                
                asset_meta = spec.get('asset_meta', {})
                asset_id = asset_meta.get('asset_id', 'unknown')
                
                # 同じ asset_id なら最新のみ保持
                if asset_id not in assets_dict:
                    asset_entry = {
                        'asset_id': asset_id,
                        'title': asset_meta.get('title', 'Untitled'),
                        'language': asset_meta.get('language', 'unknown'),
                        'status': asset_meta.get('status', 'draft'),
                        'created_at': asset_meta.get('created_at', ''),
                        'spec_file': str(spec_file),
                        'html_file': str(self.exports_dir / f"{asset_id}_manual.html"),
                        'pdf_file': str(self.exports_dir / f"{asset_id}_manual.pdf"),
                    }
                    assets_dict[asset_id] = asset_entry
            except Exception as e:
                print(f"Error processing {spec_file}: {e}")
        
        assets = list(assets_dict.values())
        return sorted(assets, key=lambda x: x.get('created_at', ''), reverse=True)
    
    def scan_booklets(self) -> List[Dict[str, Any]]:
        '''冊子をスキャンしてリスト化（重複排除）'''
        booklets_dict = {}
        
        if not self.exports_dir.exists():
            return []
        
        # _compiled.json ファイルを探す
        for compiled_file in self.exports_dir.glob("*_compiled.json"):
            try:
                with open(compiled_file, 'r', encoding='utf-8') as f:
                    compiled = json.load(f)
                
                project_id = compiled.get('project_id', 'unknown')
                
                # 同じ project_id なら最新のみ保持
                if project_id not in booklets_dict:
                    booklet_entry = {
                        'project_id': project_id,
                        'title': compiled.get('title', 'Untitled'),
                        'asset_count': compiled.get('asset_count', 0),
                        'created_at': compiled.get('created_at', ''),
                        'compiled_file': str(compiled_file),
                        'html_file': str(self.exports_dir / f"{project_id}_booklet.html"),
                        'pdf_file': str(self.exports_dir / f"{project_id}_booklet.pdf"),
                    }
                    booklets_dict[project_id] = booklet_entry
            except Exception as e:
                print(f"Error processing {compiled_file}: {e}")
        
        booklets = list(booklets_dict.values())
        return sorted(booklets, key=lambda x: x.get('created_at', ''), reverse=True)
"""

Path("src/video_asset_manualize/asset_indexer.py").write_text(asset_indexer_code, encoding='utf-8')
print("OK: asset_indexer.py fixed - deduplication added")
