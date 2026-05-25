'''
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
