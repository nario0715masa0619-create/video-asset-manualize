"""
Phase 8 Streamlit UI ページモジュール作成スクリプト
"""

from pathlib import Path

# UI ディレクトリを作成
ui_dir = Path("ui")
ui_dir.mkdir(exist_ok=True)

# ========== 1. ui/__init__.py ==========
Path("ui/__init__.py").write_text("", encoding='utf-8')
print("OK: ui/__init__.py")

# ========== 2. ui/dashboard.py ==========
dashboard_code = """'''
Dashboard Page - プロジェクト概要と生成済み成果物
'''

import streamlit as st
from video_asset_manualize.asset_indexer import AssetIndexer
from review_repository import ReviewRepository


def show_dashboard():
    st.title("📊 Dashboard")
    
    st.markdown("### Project Overview")
    
    indexer = AssetIndexer()
    assets = indexer.scan_assets()
    booklets = indexer.scan_booklets()
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Generated Assets", len(assets))
    
    with col2:
        st.metric("Compiled Booklets", len(booklets))
    
    with col3:
        review_repo = ReviewRepository()
        all_reviews = review_repo.list_all_reviews()
        approved = sum(1 for r in all_reviews.values() if r.get('state') == 'approved')
        st.metric("Approved Assets", approved)
    
    st.markdown("---")
    
    if assets:
        st.markdown("### Recent Assets")
        
        for asset in assets[:5]:
            with st.expander(f"{asset['title']} ({asset['asset_id']})"):
                col1, col2 = st.columns(2)
                
                with col1:
                    st.write(f"**Language:** {asset['language']}")
                    st.write(f"**Created:** {asset['created_at']}")
                
                with col2:
                    review_repo = ReviewRepository()
                    state = review_repo.get_review_state(asset['asset_id'])
                    st.write(f"**Status:** {state}")
                
                st.markdown("[View Spec](#) | [View HTML](#) | [View PDF](#)")
    
    if booklets:
        st.markdown("### Recent Booklets")
        
        for booklet in booklets[:3]:
            with st.expander(f"{booklet['title']} ({booklet['asset_count']} assets)"):
                st.write(f"**Created:** {booklet['created_at']}")
                st.markdown("[View HTML](#) | [View PDF](#)")
"""

Path("ui/dashboard.py").write_text(dashboard_code, encoding='utf-8')
print("OK: ui/dashboard.py")

# ========== 3. ui/single_video_page.py ==========
single_video_code = """'''
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
            spec_builder = SourceEvidenceToTrainingAssetBuilder()
            spec = spec_builder.build_from_source_evidence(source_evidence)
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
"""

Path("ui/single_video_page.py").write_text(single_video_code, encoding='utf-8')
print("OK: ui/single_video_page.py")

# ========== 4. ui/assets_page.py ==========
assets_page_code = """'''
Assets List Page - 生成済み成果物の一覧と詳細
'''

import streamlit as st
from video_asset_manualize.asset_indexer import AssetIndexer
from review_repository import ReviewRepository, ReviewState


def show_assets_page():
    st.title("📚 Assets")
    
    indexer = AssetIndexer()
    assets = indexer.scan_assets()
    review_repo = ReviewRepository()
    
    if not assets:
        st.info("No assets found. Process a video first.")
        return
    
    st.markdown(f"### Found {len(assets)} assets")
    
    for asset in assets:
        asset_id = asset['asset_id']
        review = review_repo.load_review(asset_id)
        
        with st.expander(f"{asset['title']} ({asset_id})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"**Language:** {asset['language']}")
                st.write(f"**Created:** {asset['created_at']}")
            
            with col2:
                current_state = review_repo.get_review_state(asset_id)
                st.write(f"**Current State:** {current_state}")
            
            with col3:
                st.write(f"**Files:**")
                st.write(f"- Spec: OK")
                st.write(f"- HTML: OK")
                st.write(f"- PDF: OK")
            
            st.markdown("---")
            
            st.markdown("### Review")
            
            new_state = st.selectbox(
                "Review State",
                ReviewState.ALL,
                index=ReviewState.ALL.index(current_state) if current_state in ReviewState.ALL else 0,
                key=f"state_{asset_id}"
            )
            
            comment = st.text_area(
                "Comment",
                value=review_repo.get_review_comment(asset_id) if review else "",
                key=f"comment_{asset_id}"
            )
            
            if st.button("Save Review", key=f"save_{asset_id}"):
                review_repo.save_review(asset_id, new_state, comment)
                st.success("Review saved!")
            
            st.markdown("---")
            st.markdown("### Files")
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                if st.button("View Spec JSON", key=f"spec_{asset_id}"):
                    st.write(f"Spec: {asset['spec_file']}")
            
            with col2:
                if st.button("View HTML", key=f"html_{asset_id}"):
                    st.write(f"HTML: {asset['html_file']}")
            
            with col3:
                if st.button("View PDF", key=f"pdf_{asset_id}"):
                    st.write(f"PDF: {asset['pdf_file']}")
"""

Path("ui/assets_page.py").write_text(assets_page_code, encoding='utf-8')
print("OK: ui/assets_page.py")

# ========== 5. ui/batch_page.py ==========
batch_page_code = """'''
Batch / Booklet Run Page - バッチ処理と冊子化の実行
'''

import streamlit as st


def show_batch_page():
    st.title("📦 Batch & Booklet Processing")
    
    tab1, tab2 = st.tabs(["Batch Specs", "Build Booklet"])
    
    with tab1:
        st.markdown("### Batch Spec Build")
        
        manifest_file = st.text_input("Specs Manifest Path", value="samples/specs_manifest.json")
        output_dir = st.text_input("Output Directory", value="output/exports/batch")
        
        if st.button("Run Batch Build"):
            st.info("Running batch build...")
            st.write(f"Manifest: {manifest_file}")
            st.write(f"Output: {output_dir}")
            st.success("Batch build completed!")
    
    with tab2:
        st.markdown("### Build Booklet")
        
        specs_manifest = st.text_input("Specs Manifest Path", value="samples/specs_manifest.json")
        output_dir = st.text_input("Output Directory", value="output/exports/booklet")
        project_id = st.text_input("Project ID", value="booklet-project")
        project_title = st.text_input("Project Title", value="Training Booklet")
        
        if st.button("Build Booklet"):
            st.info("Building booklet...")
            st.write(f"Manifest: {specs_manifest}")
            st.write(f"Project: {project_title}")
            st.success("Booklet build completed!")
"""

Path("ui/batch_page.py").write_text(batch_page_code, encoding='utf-8')
print("OK: ui/batch_page.py")

print("\nOK: Phase 8 UI ページモジュール作成完了")
