'''
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
        '''成果物をスキャンしてリスト化'''
        assets = []
        
        if not self.exports_dir.exists():
            return assets
        
        # _spec.json ファイルを探す
        for spec_file in self.exports_dir.glob("*_spec.json"):
            try:
                with open(spec_file, 'r', encoding='utf-8') as f:
                    spec = json.load(f)
                
                asset_meta = spec.get('asset_meta', {})
                asset_id = asset_meta.get('asset_id', 'unknown')
                
                # 対応するファイルを探す
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
                
                assets.append(asset_entry)
            except Exception as e:
                print(f"Error processing {spec_file}: {e}")
        
        return sorted(assets, key=lambda x: x.get('created_at', ''), reverse=True)
    
    def scan_booklets(self) -> List[Dict[str, Any]]:
        '''冊子をスキャンしてリスト化'''
        booklets = []
        
        if not self.exports_dir.exists():
            return booklets
        
        # _compiled.json ファイルを探す
        for compiled_file in self.exports_dir.glob("*_compiled.json"):
            try:
                with open(compiled_file, 'r', encoding='utf-8') as f:
                    compiled = json.load(f)
                
                project_id = compiled.get('project_id', 'unknown')
                
                booklet_entry = {
                    'project_id': project_id,
                    'title': compiled.get('title', 'Untitled'),
                    'asset_count': compiled.get('asset_count', 0),
                    'created_at': compiled.get('created_at', ''),
                    'compiled_file': str(compiled_file),
                    'html_file': str(self.exports_dir / f"{project_id}_booklet.html"),
                    'pdf_file': str(self.exports_dir / f"{project_id}_booklet.pdf"),
                }
                
                booklets.append(booklet_entry)
            except Exception as e:
                print(f"Error processing {compiled_file}: {e}")
        
        return sorted(booklets, key=lambda x: x.get('created_at', ''), reverse=True)
