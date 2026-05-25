'''
Batch Manifest Loader - 複数入力の manifest JSON を解析
'''

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from dataclasses import dataclass


@dataclass
class VideoManifestItem:
    '''動画 manifest のアイテム'''
    video_id: str
    input_path: str
    title: Optional[str] = None
    audience: Optional[List[str]] = None
    
    def validate(self) -> bool:
        '''入力ファイルの存在を確認'''
        return Path(self.input_path).exists()


@dataclass
class SpecManifestItem:
    '''Spec manifest のアイテム'''
    asset_id: str
    spec_path: str
    title: Optional[str] = None
    
    def validate(self) -> bool:
        '''入力ファイルの存在を確認'''
        return Path(self.spec_path).exists()


class BatchManifestLoader:
    '''Manifest JSON を読み込んで Item リストに変換'''
    
    @staticmethod
    def load_videos_manifest(manifest_path: str) -> tuple[str, str, List[VideoManifestItem]]:
        '''動画 manifest を読み込む
        
        Returns:
            (project_id, title, items)
        '''
        manifest_path = Path(manifest_path)
        
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        project_id = data.get('project_id', 'project-default')
        title = data.get('title', 'Untitled Project')
        items_data = data.get('items', [])
        
        items = [
            VideoManifestItem(
                video_id=item['video_id'],
                input_path=item['input_path'],
                title=item.get('title'),
                audience=item.get('audience', [])
            )
            for item in items_data
        ]
        
        return project_id, title, items
    
    @staticmethod
    def load_specs_manifest(manifest_path: str) -> tuple[str, str, List[SpecManifestItem]]:
        '''Spec manifest を読み込む
        
        Returns:
            (project_id, title, items)
        '''
        manifest_path = Path(manifest_path)
        
        if not manifest_path.exists():
            raise FileNotFoundError(f"Manifest not found: {manifest_path}")
        
        with open(manifest_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        project_id = data.get('project_id', 'project-default')
        title = data.get('title', 'Untitled Project')
        items_data = data.get('items', [])
        
        items = [
            SpecManifestItem(
                asset_id=item['asset_id'],
                spec_path=item['spec_path'],
                title=item.get('title')
            )
            for item in items_data
        ]
        
        return project_id, title, items
    
    @staticmethod
    def validate_items(items: List[Any]) -> tuple[List[Any], List[tuple[int, str]]]:
        '''アイテムの存在確認
        
        Returns:
            (valid_items, [(index, error_message)])
        '''
        valid_items = []
        errors = []
        
        for idx, item in enumerate(items):
            if item.validate():
                valid_items.append(item)
            else:
                errors.append((idx, f"File not found: {item.input_path if hasattr(item, 'input_path') else item.spec_path}"))
        
        return valid_items, errors
