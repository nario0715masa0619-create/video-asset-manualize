"""
Phase 8 Web UI 基盤モジュール自動生成スクリプト
"""

from pathlib import Path

# ========== 1. review_repository.py ==========
review_repo_code = """'''
Review Repository - レビュー状態とコメントの管理
'''

import json
from pathlib import Path
from typing import Dict, Any, Optional
from datetime import datetime


class ReviewState:
    '''アセットのレビュー状態'''
    
    DRAFT = "draft"
    IN_REVIEW = "in_review"
    APPROVED = "approved"
    REJECTED = "rejected"
    
    ALL = [DRAFT, IN_REVIEW, APPROVED, REJECTED]


class ReviewRepository:
    '''レビュー状態をファイルベースで管理'''
    
    def __init__(self, storage_dir: str = "data/reviews"):
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
    
    def save_review(self, asset_id: str, state: str, comment: str = ""):
        '''レビュー状態を保存'''
        review_data = {
            'asset_id': asset_id,
            'state': state,
            'comment': comment,
            'updated_at': datetime.utcnow().isoformat() + 'Z'
        }
        
        review_file = self.storage_dir / f"{asset_id}_review.json"
        
        with open(review_file, 'w', encoding='utf-8') as f:
            json.dump(review_data, f, ensure_ascii=False, indent=2)
    
    def load_review(self, asset_id: str) -> Optional[Dict[str, Any]]:
        '''レビュー状態を読み込む'''
        review_file = self.storage_dir / f"{asset_id}_review.json"
        
        if not review_file.exists():
            return None
        
        with open(review_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def get_review_state(self, asset_id: str) -> str:
        '''レビュー状態を取得（デフォルト: draft）'''
        review = self.load_review(asset_id)
        return review.get('state', ReviewState.DRAFT) if review else ReviewState.DRAFT
    
    def get_review_comment(self, asset_id: str) -> str:
        '''レビューコメントを取得'''
        review = self.load_review(asset_id)
        return review.get('comment', '') if review else ''
    
    def list_all_reviews(self) -> Dict[str, Dict[str, Any]]:
        '''すべてのレビューを取得'''
        reviews = {}
        
        for review_file in self.storage_dir.glob("*_review.json"):
            with open(review_file, 'r', encoding='utf-8') as f:
                review_data = json.load(f)
                asset_id = review_data.get('asset_id', '')
                reviews[asset_id] = review_data
        
        return reviews
"""

Path("src/video_asset_manualize/review_repository.py").write_text(review_repo_code, encoding='utf-8')
print("OK: review_repository.py")

# ========== 2. asset_indexer.py ==========
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
"""

Path("src/video_asset_manualize/asset_indexer.py").write_text(asset_indexer_code, encoding='utf-8')
print("OK: asset_indexer.py")

print("\nOK: Phase 8 基盤モジュール作成完了")
