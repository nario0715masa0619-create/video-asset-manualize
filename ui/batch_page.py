'''
Batch / Booklet Run Page - バッチ処理と冊子化の実行
'''

import streamlit as st
import json
from pathlib import Path
from video_asset_manualize.ui_pipeline_runner import UIPipelineRunner
from video_asset_manualize.batch_manifest_loader import BatchManifestLoader


def _check_modes(manifest_file: str):
    """Check specs in manifest for non-canonical generation modes."""
    try:
        _, _, specs = BatchManifestLoader.load_specs_manifest(manifest_file)
        has_non_canonical = False
        has_weak_evidence = False
        modes = set()
        modalities = set()
        
        for spec_item in specs:
            spec_path = Path(spec_item.spec_path)
            if spec_path.exists():
                with open(spec_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    mode = data.get("metadata", {}).get("generation_mode", "unknown")
                    modality = data.get("metadata", {}).get("dominant_modality", "unknown")
                    quality = data.get("metadata", {}).get("evidence_quality", "unknown")
                    modes.add(mode)
                    modalities.add(modality)
                    if mode != "canonical":
                        has_non_canonical = True
                    if modality == "weak_evidence" or quality == "weak":
                        has_weak_evidence = True
                        
        if has_non_canonical:
            st.warning(f"⚠️ 対象に非正本 (non-canonical) spec が含まれています。Modes: {', '.join(modes)}")
        elif "canonical" in modes:
            st.success("🟢 全ての spec が canonical (Production-ready) です。")
            
        if has_weak_evidence:
            st.warning("⚠️ 対象に証拠不十分 (weak_evidence) の spec が含まれています。目視レビューが必要です。")
    except Exception:
        pass


def show_batch_page():
    st.title("Batch & Booklet Processing")
    
    runner = UIPipelineRunner()
    
    tab1, tab2 = st.tabs(["Batch Specs", "Build Booklet"])
    
    with tab1:
        st.markdown("### Batch Spec Build")
        st.markdown("複数の JSON スペックから HTML と PDF マニュアルを一括生成します。")
        
        manifest_file = st.text_input("Specs Manifest Path", value="samples/specs_manifest_batch_test.json", key="batch_manifest")
        output_dir = st.text_input("Output Directory", value="output/exports/batch", key="batch_output")
        
        if st.button("Run Batch Build", key="run_batch"):
            _check_modes(manifest_file)
            st.info("Running batch build...")
            result = runner.run_batch_specs(manifest_file, output_dir)
            
            if result.success:
                st.success(result.message)
                st.write(f"処理件数: {result.item_count} 件 (成功: {result.item_count - result.failure_count}, 失敗: {result.failure_count})")
                
                if "report" in result.files:
                    report_path = Path(result.files["report"])
                    if report_path.exists():
                        with open(report_path, "rb") as f:
                            st.download_button(
                                label="📄 ダウンロード Batch Report (JSON)",
                                data=f,
                                file_name="batch_report.json",
                                use_container_width=True
                            )
            else:
                st.error(result.message)
                if result.error_message:
                    with st.expander("Technical Details (Traceback)"):
                        st.code(result.error_message, language="python")
            
            with st.expander("実行ログ"):
                for log in result.logs:
                    st.text(log)
    
    with tab2:
        st.markdown("### Build Booklet")
        st.markdown("複数のマニュアルを結合し、1つの冊子 (HTML/PDF) として出力します。")
        
        specs_manifest = st.text_input("Specs Manifest Path", value="samples/specs_manifest_batch_test.json", key="booklet_manifest")
        output_dir_booklet = st.text_input("Output Directory", value="output/exports/booklet", key="booklet_output")
        project_id = st.text_input("Project ID", value="booklet-project", key="project_id")
        project_title = st.text_input("Project Title", value="Training Booklet", key="project_title")
        
        if st.button("Build Booklet", key="build_booklet"):
            _check_modes(specs_manifest)
            st.info("Building booklet...")
            result = runner.run_booklet_build(specs_manifest, output_dir_booklet, project_id, project_title)
            
            if result.success:
                st.success(result.message)
                st.write(f"結合したマニュアル数: {result.item_count} 件")
                
                dl_col1, dl_col2, dl_col3 = st.columns(3)
                
                if "compiled_json" in result.files:
                    path = Path(result.files["compiled_json"])
                    if path.exists():
                        with open(path, "rb") as f:
                            dl_col1.download_button(label="📄 Compiled JSON", data=f, file_name=f"{project_id}_compiled.json", use_container_width=True)
                            
                if "booklet_html" in result.files:
                    path = Path(result.files["booklet_html"])
                    if path.exists():
                        with open(path, "rb") as f:
                            dl_col2.download_button(label="🌐 Booklet HTML", data=f, file_name=f"{project_id}_booklet.html", mime="text/html", use_container_width=True)
                            
                if "booklet_pdf" in result.files:
                    path = Path(result.files["booklet_pdf"])
                    if path.exists():
                        with open(path, "rb") as f:
                            dl_col3.download_button(label="📋 Booklet PDF", data=f, file_name=f"{project_id}_booklet.pdf", mime="application/pdf", use_container_width=True)
            else:
                st.error(result.message)
                if result.error_message:
                    with st.expander("Technical Details (Traceback)"):
                        st.code(result.error_message, language="python")
                        
            with st.expander("実行ログ"):
                for log in result.logs:
                    st.text(log)
