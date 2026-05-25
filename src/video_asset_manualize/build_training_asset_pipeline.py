'''
Build Training Asset Pipeline
'''

from pathlib import Path
from typing import Dict, Any, Optional
from video_asset_manualize.schema_validator import SchemaValidator
from video_asset_manualize.training_asset_spec_builder import TrainingAssetSpecBuilder
from video_asset_manualize.html_manual_renderer import HTMLManualRenderer
from video_asset_manualize.pdf_manual_renderer import PDFManualRenderer
from video_asset_manualize import settings
import json


class BuildTrainingAssetPipeline:
    '''Training Asset Spec をビルドして HTML/PDF を生成'''
    
    def __init__(self):
        self.validator = SchemaValidator()
        self.spec_builder = TrainingAssetSpecBuilder()
        self.html_renderer = HTMLManualRenderer()
        self.pdf_renderer = PDFManualRenderer()
        self.spec = None
    
    def load_spec(self, input_file: str) -> Dict[str, Any]:
        '''Spec JSON をロード'''
        input_path = Path(input_file)
        
        with open(input_path, 'r', encoding='utf-8') as f:
            self.spec = json.load(f)
        
        return self.spec
    
    def validate(self) -> bool:
        '''Spec を検証'''
        if self.spec is None:
            raise ValueError("No spec loaded")
        
        self.validator.validate(self.spec)
        return True
    
    def generate_outputs(
        self,
        input_file: str,
        output_dir: Optional[str] = None,
        format: str = "all"
    ) -> Dict[str, Optional[str]]:
        '''フルパイプライン - ロード、検証、ビルド'''
        
        # Output directory setup
        if output_dir is None:
            output_dir = settings.settings.EXPORTS_DIR
        
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Load
        self.load_spec(input_file)
        
        # Validate
        self.validate()
        
        # Generate outputs
        results = {}
        
        if format in ["html", "all"]:
            asset_id = self.spec.get('asset_meta', {}).get('asset_id', 'manual')
            html_file = f"{asset_id}_manual.html"
            html_path = output_dir / html_file
            
            self.html_renderer.render_to_file(self.spec, html_path)
            
            results['html'] = str(html_path)
        else:
            results['html'] = None
        
        if format in ["pdf", "all"]:
            asset_id = self.spec.get('asset_meta', {}).get('asset_id', 'manual')
            pdf_file = f"{asset_id}_manual.pdf"
            pdf_path = output_dir / pdf_file
            
            self.pdf_renderer.render_to_file(self.spec, pdf_path)
            
            results['pdf'] = str(pdf_path)
        else:
            results['pdf'] = None
        
        # Save spec as JSON
        asset_id = self.spec.get('asset_meta', {}).get('asset_id', 'spec')
        spec_file = f"{asset_id}_spec.json"
        spec_path = output_dir / spec_file
        
        with open(spec_path, 'w', encoding='utf-8') as f:
            json.dump(self.spec, f, ensure_ascii=False, indent=2)
        
        results['json'] = str(spec_path)
        
        return results
