"""
UI Pipeline Runner - CLI パイプラインを UI から呼び出すラッパー
Phase 9: UI から直接実行可能にする
"""

from pathlib import Path
from typing import Dict, Optional, Tuple
import json
from datetime import datetime

from video_asset_manualize.video_source_evidence_builder import VideoSourceEvidenceBuilder
from video_asset_manualize.source_evidence_to_training_asset_builder import SourceEvidenceToTrainingAssetBuilder
from video_asset_manualize.build_training_asset_pipeline import BuildTrainingAssetPipeline


class UIExecutionResult:
    """UI 実行結果を統一的に管理"""

    def __init__(self):
        self.success = False
        self.message = ""
        self.error_message = ""
        self.files = {}  # {file_type: file_path}
        self.asset_id = None
        self.logs = []
        self.item_count = 0
        self.failure_count = 0

    def add_log(self, message: str):
        """ログ追加"""
        timestamp = datetime.now().strftime('%H:%M:%S')
        self.logs.append(f"[{timestamp}] {message}")


class UIPipelineRunner:
    """UIからの実行を管理するランナークラス"""
    
    def __init__(self):
        self.output_dir = Path("output/exports")
        self.output_dir.mkdir(parents=True, exist_ok=True)
        
    def run_single_video_pipeline(self, video_path: str, use_llm: bool, llm_provider: str, transcript_provider: str, ocr_provider: str) -> UIExecutionResult:
        result = UIExecutionResult()
        
        try:
            result.add_log("Step 1: Extracting source evidence...")
            evidence_builder = VideoSourceEvidenceBuilder()
            source_evidence = evidence_builder.build_from_video(video_path)
            result.add_log("Source evidence extracted successfully.")
            
            result.add_log("Step 2: Building training asset spec...")
            if use_llm:
                from video_asset_manualize.llm_training_asset_builder import LLMTrainingAssetBuilder
                from video_asset_manualize.provider_factory import ProviderFactory
                llm_provider_obj = ProviderFactory.create_llm_provider(provider_type=llm_provider)
                spec_builder = LLMTrainingAssetBuilder(llm_provider=llm_provider_obj)
                spec = spec_builder.build_from_source_evidence(source_evidence)
            else:
                from video_asset_manualize.source_evidence_to_training_asset_builder import SourceEvidenceToTrainingAssetBuilder
                spec_builder = SourceEvidenceToTrainingAssetBuilder()
                spec_builder.source_evidence = source_evidence
                spec = spec_builder.build_training_asset_spec()
            result.add_log("Spec built successfully.")
            
            result.add_log("Step 3: Generating HTML/PDF outputs...")
            asset_id = spec.get('asset_meta', {}).get('asset_id', 'unknown')
            result.asset_id = asset_id
            
            spec_file = self.output_dir / f"{asset_id}_spec.json"
            with open(spec_file, 'w', encoding='utf-8') as f:
                json.dump(spec, f, ensure_ascii=False, indent=2)
                
            pipeline = BuildTrainingAssetPipeline()
            outputs = pipeline.generate_outputs(str(spec_file), output_dir=str(self.output_dir))
            
            result.success = True
            result.message = "Processing complete!"
            result.files = outputs
            result.add_log("Pipeline completed successfully.")
            
        except Exception as e:
            result.success = False
            result.error_message = str(e)
            result.add_log(f"Error occurred: {str(e)}")
            
        return result

    def run_batch_specs(self, manifest_file: str, output_dir: str) -> UIExecutionResult:
        from video_asset_manualize.batch_manifest_loader import BatchManifestLoader
        from video_asset_manualize.batch_pipeline import BatchPipeline
        import traceback
        
        result = UIExecutionResult()
        try:
            result.add_log(f"Starting batch specs using manifest: {manifest_file}")
            
            manifest_path = Path(manifest_file)
            if not manifest_path.exists():
                raise FileNotFoundError(f"マニフェストファイルが見つかりません: {manifest_file}")
            
            project_id, title, specs = BatchManifestLoader.load_specs_manifest(manifest_file)
            result.add_log(f"Loaded project: {title} ({project_id})")
            
            valid_specs, errors = BatchManifestLoader.validate_items(specs)
            if errors:
                result.add_log(f"Validation found {len(errors)} errors.")
                for idx, err in errors:
                    result.add_log(f"Item {idx} error: {err}")
            
            result.item_count = len(specs)
            
            pipeline = BatchPipeline()
            report, outputs = pipeline.process_specs_batch(valid_specs, output_dir)
            
            result.failure_count = report.failed
            
            report_file = Path(output_dir) / "batch_report.json"
            report.save(str(report_file))
            result.add_log(f"Saved batch report to {report_file}")
            
            result.success = True
            result.message = f"Batch build completed: {report.succeeded} succeeded, {report.failed} failed."
            result.files = {"report": str(report_file)}
            
        except Exception as e:
            result.success = False
            result.message = f"エラーが発生しました: {str(e)}"
            result.error_message = traceback.format_exc()
            result.add_log(f"Error: {str(e)}")
            
        return result

    def run_booklet_build(self, specs_manifest: str, output_dir: str, project_id: str, project_title: str) -> UIExecutionResult:
        from video_asset_manualize.batch_manifest_loader import BatchManifestLoader
        from video_asset_manualize.compiled_training_asset_builder import CompiledTrainingAssetBuilder
        from video_asset_manualize.booklet_html_renderer import BookletHTMLRenderer
        from video_asset_manualize.booklet_pdf_renderer import BookletPDFRenderer
        import traceback
        
        result = UIExecutionResult()
        try:
            result.add_log(f"Starting booklet build using manifest: {specs_manifest}")
            
            manifest_path = Path(specs_manifest)
            if not manifest_path.exists():
                raise FileNotFoundError(f"マニフェストファイルが見つかりません: {specs_manifest}")
                
            _, _, specs = BatchManifestLoader.load_specs_manifest(specs_manifest)
            valid_specs, errors = BatchManifestLoader.validate_items(specs)
            
            result.item_count = len(valid_specs)
            
            spec_dicts = []
            for spec_item in valid_specs:
                with open(spec_item.spec_path, 'r', encoding='utf-8') as f:
                    spec_dicts.append(json.load(f))
            
            result.add_log(f"Loaded {len(spec_dicts)} spec files.")
            
            compiled = CompiledTrainingAssetBuilder.compile_specs(
                spec_dicts,
                project_id=project_id,
                title=project_title,
                description="Compiled Training Manual"
            )
            
            out_path = Path(output_dir)
            out_path.mkdir(parents=True, exist_ok=True)
            
            compiled_file = out_path / f"{project_id}_compiled.json"
            compiled.save(str(compiled_file))
            result.files['compiled_json'] = str(compiled_file)
            result.add_log("Compiled JSON saved.")
            
            html_renderer = BookletHTMLRenderer()
            html_file = out_path / f"{project_id}_booklet.html"
            html_renderer.render_to_file(compiled, str(html_file))
            result.files['booklet_html'] = str(html_file)
            result.add_log("Booklet HTML generated.")
            
            pdf_renderer = BookletPDFRenderer()
            pdf_file = out_path / f"{project_id}_booklet.pdf"
            pdf_renderer.render_to_file(compiled, str(pdf_file))
            result.files['booklet_pdf'] = str(pdf_file)
            result.add_log("Booklet PDF generated.")
            
            result.success = True
            result.message = "Booklet build completed successfully."
            
        except Exception as e:
            result.success = False
            result.message = f"エラーが発生しました: {str(e)}"
            result.error_message = traceback.format_exc()
            result.add_log(f"Error: {str(e)}")
            
        return result
