'''
Single Video Run Page - 単一動画の処理実行
'''

import streamlit as st
from pathlib import Path
from video_asset_manualize.video_source_evidence_builder import VideoSourceEvidenceBuilder
from video_asset_manualize.source_evidence_to_training_asset_builder import SourceEvidenceToTrainingAssetBuilder
from video_asset_manualize.build_training_asset_pipeline import BuildTrainingAssetPipeline


def show_single_video_page():
    st.title("🎬 Single Video Processing")
    
    st.markdown("### Input")
    
    col1, col2 = st.columns(2)
    
    with col1:
        video_path = st.text_input("Video File Path", value="samples/sample_training_video.mp4")
    
    with col2:
        use_llm = st.checkbox("Use LLM Extraction", value=False)
    
    if use_llm:
        llm_provider = st.selectbox("LLM Provider", ["dummy", "openai"])
    else:
        llm_provider = "dummy"
    
    transcript_provider = st.selectbox("Transcript Provider", ["dummy", "whisper"])
    ocr_provider = st.selectbox("OCR Provider", ["dummy", "easyocr"])
    
    if st.button("Process Video", key="process_video"):
        st.info("Processing video...")
        
        try:
            # Extract source_evidence
            st.write("Step 1: Extracting source evidence...")
            evidence_builder = VideoSourceEvidenceBuilder()
            source_evidence = evidence_builder.build_from_video(video_path)
            st.success("Source evidence extracted")
            
            # Build spec
            st.write("Step 2: Building training asset spec...")
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
            st.success("Spec built")
            
            # Save and generate
            st.write("Step 3: Generating HTML/PDF...")
            import json
            from pathlib import Path
            
            output_dir = Path("output/exports")
            output_dir.mkdir(parents=True, exist_ok=True)
            
            asset_id = spec.get('asset_meta', {}).get('asset_id', 'unknown')
            spec_file = output_dir / f"{asset_id}_spec.json"
            
            with open(spec_file, 'w', encoding='utf-8') as f:
                json.dump(spec, f, ensure_ascii=False, indent=2)
            
            pipeline = BuildTrainingAssetPipeline()
            results = pipeline.generate_outputs(str(spec_file), output_dir=str(output_dir))
            
            st.success("Processing complete!")
            
            st.markdown("### Results")
            st.write(f"**Asset ID:** {asset_id}")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if results.get('html'):
                    st.markdown(f"[📄 View HTML]({results['html']})")
            
            with col2:
                if results.get('pdf'):
                    st.markdown(f"[📋 View PDF]({results['pdf']})")
            
            with col3:
                if results.get('json'):
                    st.markdown(f"[📝 View JSON]({results['json']})")
        
        except Exception as e:
            st.error(f"Error: {str(e)}")
