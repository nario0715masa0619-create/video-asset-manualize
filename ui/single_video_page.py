'''
Single Video Run Page - 単一動画の処理実行
'''

from pathlib import Path
import streamlit as st
from video_asset_manualize.video_source_evidence_builder import VideoSourceEvidenceBuilder
from video_asset_manualize.build_training_asset_pipeline import BuildTrainingAssetPipeline
from video_asset_manualize.orchestration import Orchestrator
from video_asset_manualize.generation_mode import GenerationMode


def show_single_video_page():
    st.title("🎬 Single Video Processing")
    
    st.markdown("### Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        video_path = st.text_input("Video File Path", value="samples/sample_training_video.mp4")
    
    with col2:
        mode_str = st.selectbox("Generation Mode", ["canonical", "fallback", "test"], index=0)
    
    if mode_str == "canonical":
        llm_provider = st.selectbox("LLM Provider", ["openai", "dummy"], index=0)
    else:
        llm_provider = "dummy"
    
    transcript_provider = st.selectbox("Transcript Provider", ["whisper", "dummy"], index=0)
    ocr_provider = st.selectbox("OCR Provider", ["easyocr", "dummy"], index=0)
    
    if "single_video_processing_result" not in st.session_state:
        st.session_state.single_video_processing_result = None
    
    if st.button("Process Video", key="process_video"):
        st.info("Processing video...")
        
        try:
            # Extract source_evidence
            st.write("Step 1: Extracting source evidence...")
            evidence_builder = VideoSourceEvidenceBuilder()
            source_evidence = evidence_builder.build_from_video(video_path)
            st.success("Source evidence extracted")
            
            # Temporary save for orchestration (Orchestrator takes file path)
            import json
            temp_dir = Path("output/temp")
            temp_dir.mkdir(parents=True, exist_ok=True)
            temp_evidence = temp_dir / "temp_evidence.json"
            with open(temp_evidence, 'w', encoding='utf-8') as f:
                json.dump(source_evidence, f, ensure_ascii=False)
            
            # Build spec via Orchestrator
            st.write(f"Step 2: Building training asset spec ({mode_str} mode)...")
            gen_mode = Orchestrator.resolve_generation_mode(mode_str)
            spec = Orchestrator.extract_with_mode(
                source_evidence_path=str(temp_evidence),
                mode=gen_mode,
                llm_provider_name=llm_provider
            )
            st.success("Spec built")
            
            # Save and generate
            st.write("Step 3: Generating HTML/PDF...")
            output_dir = Path("output/exports")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            asset_id = spec.get('asset_meta', {}).get('asset_id', 'unknown')
            spec_file = output_dir / f"{asset_id}_spec.json"
            
            with open(spec_file, 'w', encoding='utf-8') as f:
                json.dump(spec, f, ensure_ascii=False, indent=2)
            
            pipeline = BuildTrainingAssetPipeline()
            results = pipeline.generate_outputs(str(spec_file), output_dir=str(output_dir))
            
            st.session_state.single_video_processing_result = {
                "results": results,
                "asset_id": asset_id,
                "mode": mode_str,
                "provider": spec.get('metadata', {}).get('provider', 'n/a')
            }
            st.success("Processing complete!")
            
        except Exception as e:
            st.error(f"Error: {str(e)}")
            st.session_state.single_video_processing_result = None
            
    if st.session_state.single_video_processing_result:
        data = st.session_state.single_video_processing_result
        results = data["results"]
        asset_id = data["asset_id"]
        mode = data.get("mode", "unknown")
        
        st.markdown("### Results")
        
        # Display Mode Warnings
        if mode == "canonical":
            st.success(f"**Generation Mode:** CANONICAL (Production Ready) - Provider: {data.get('provider')}")
        elif mode in ["fallback", "test"]:
            st.warning(f"**Generation Mode:** {mode.upper()} - ⚠️ この spec は production canonical ではありません。正本として扱うには canonical generation を実行してください。")
        else:
            st.error("**Generation Mode:** UNKNOWN - ⚠️ この spec は非 canonical です。")
            
        st.write(f"**Asset ID:** {asset_id}")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if results.get('html'):
                html_path = Path(results['html'])
                if html_path.exists():
                    with open(html_path, 'r', encoding='utf-8') as html_file:
                        st.download_button(
                            label="📥 Download HTML",
                            data=html_file.read(),
                            file_name=html_path.name,
                            mime="text/html",
                            key="download_html_single_video"
                        )
                else:
                    st.error("⚠️ HTML ファイルが見つかりません")
        
        with col2:
            if results.get('pdf'):
                pdf_path = Path(results['pdf'])
                if pdf_path.exists():
                    with open(pdf_path, 'rb') as pdf_file:
                        st.download_button(
                            label="📥 Download PDF",
                            data=pdf_file.read(),
                            file_name=pdf_path.name,
                            mime="application/pdf",
                            key="download_pdf_single_video"
                        )
                else:
                    st.error("⚠️ PDF ファイルが見つかりません")
        
        with col3:
            if results.get('json'):
                json_path = Path(results['json'])
                if json_path.exists():
                    with open(json_path, 'r', encoding='utf-8') as json_file:
                        st.download_button(
                            label="📥 Download JSON",
                            data=json_file.read(),
                            file_name=json_path.name,
                            mime="application/json",
                            key="download_json_single_video"
                        )
                else:
                    st.error("⚠️ JSON ファイルが見つかりません")
