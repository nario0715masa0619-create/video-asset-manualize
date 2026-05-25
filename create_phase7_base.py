"""
Phase 7 基盤モジュール自動生成スクリプト
"""

from pathlib import Path

# ========== 1. batch_manifest_loader.py ==========
batch_manifest_code = """'''
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
"""

Path("src/video_asset_manualize/batch_manifest_loader.py").write_text(batch_manifest_code, encoding='utf-8')
print("✓ Created: src/video_asset_manualize/batch_manifest_loader.py")

# ========== 2. batch_pipeline.py ==========
batch_pipeline_code = """'''
Batch Pipeline - 複数動画・複数 spec を逐次処理
'''

import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from datetime import datetime

from video_asset_manualize.video_source_evidence_builder import VideoSourceEvidenceBuilder
from video_asset_manualize.source_evidence_validator import SourceEvidenceValidator
from video_asset_manualize.source_evidence_to_training_asset_builder import SourceEvidenceToTrainingAssetBuilder
from video_asset_manualize.llm_training_asset_builder import LLMTrainingAssetBuilder
from video_asset_manualize.provider_factory import ProviderFactory
from video_asset_manualize.build_training_asset_pipeline import BuildTrainingAssetPipeline
from video_asset_manualize.batch_manifest_loader import BatchManifestLoader, VideoManifestItem, SpecManifestItem
from video_asset_manualize import settings


class BatchProcessingReport:
    '''バッチ処理のレポート'''
    
    def __init__(self, project_id: str, title: str):
        self.project_id = project_id
        self.title = title
        self.timestamp = datetime.utcnow().isoformat() + 'Z'
        self.total = 0
        self.succeeded = 0
        self.failed = 0
        self.results = []
        self.errors = []
    
    def add_success(self, item_id: str, outputs: Dict[str, str]):
        '''成功を記録'''
        self.succeeded += 1
        self.results.append({
            'item_id': item_id,
            'status': 'success',
            'outputs': outputs
        })
    
    def add_error(self, item_id: str, error_msg: str):
        '''エラーを記録'''
        self.failed += 1
        self.errors.append({
            'item_id': item_id,
            'error': error_msg
        })
    
    def to_dict(self) -> Dict[str, Any]:
        '''辞書に変換'''
        return {
            'project_id': self.project_id,
            'title': self.title,
            'timestamp': self.timestamp,
            'summary': {
                'total': self.total,
                'succeeded': self.succeeded,
                'failed': self.failed
            },
            'results': self.results,
            'errors': self.errors
        }
    
    def save(self, output_path: str):
        '''レポートをファイルに保存'''
        output_path = Path(output_path)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)


class BatchPipeline:
    '''複数動画またはスペックをバッチ処理'''
    
    def __init__(self):
        self.validator = SourceEvidenceValidator()
        self.evidence_builder = VideoSourceEvidenceBuilder()
        self.spec_builder = SourceEvidenceToTrainingAssetBuilder()
        self.build_pipeline = BuildTrainingAssetPipeline()
    
    def process_videos_batch(
        self,
        videos: List[VideoManifestItem],
        output_dir: str,
        use_llm: bool = False,
        llm_provider: str = "dummy"
    ) -> tuple[BatchProcessingReport, List[Dict[str, str]]]:
        '''複数動画を処理
        
        Returns:
            (report, individual_specs)
        '''
        report = BatchProcessingReport("batch-videos", "Batch Video Processing")
        report.total = len(videos)
        
        individual_specs = []
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for idx, video in enumerate(videos):
            try:
                # Step 1: Extract source_evidence
                source_evidence = self.evidence_builder.build_from_video(video.input_path)
                
                # Step 2: Build training_asset_spec
                if use_llm:
                    llm_provider_obj = ProviderFactory.create_llm_provider(provider_type=llm_provider)
                    spec_builder_obj = LLMTrainingAssetBuilder(llm_provider=llm_provider_obj)
                    spec = spec_builder_obj.build_from_source_evidence(source_evidence)
                else:
                    spec = self.spec_builder.build_from_source_evidence(source_evidence)
                
                # Step 3: Save spec
                asset_id = spec.get('asset_meta', {}).get('asset_id', f'asset-{idx}')
                spec_file = output_dir / f"{asset_id}_spec.json"
                
                with open(spec_file, 'w', encoding='utf-8') as f:
                    json.dump(spec, f, ensure_ascii=False, indent=2)
                
                outputs = {'spec': str(spec_file)}
                report.add_success(video.video_id, outputs)
                individual_specs.append(spec)
                
            except Exception as e:
                report.add_error(video.video_id, str(e))
        
        return report, individual_specs
    
    def process_specs_batch(
        self,
        specs: List[SpecManifestItem],
        output_dir: str
    ) -> tuple[BatchProcessingReport, List[Dict[str, str]]]:
        '''複数 spec をビルド（HTML/PDF 生成）
        
        Returns:
            (report, output_file_paths)
        '''
        report = BatchProcessingReport("batch-specs", "Batch Spec Build")
        report.total = len(specs)
        
        output_paths = []
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        for spec_item in specs:
            try:
                results = self.build_pipeline.generate_outputs(
                    spec_item.spec_path,
                    output_dir=str(output_dir),
                    format="all"
                )
                
                outputs = {
                    'html': results.get('html'),
                    'pdf': results.get('pdf'),
                    'json': results.get('json')
                }
                report.add_success(spec_item.asset_id, outputs)
                output_paths.append(outputs)
                
            except Exception as e:
                report.add_error(spec_item.asset_id, str(e))
        
        return report, output_paths
"""

Path("src/video_asset_manualize/batch_pipeline.py").write_text(batch_pipeline_code, encoding='utf-8')
print("✓ Created: src/video_asset_manualize/batch_pipeline.py")

print("\n✅ Phase 7 基盤モジュール作成完了")
