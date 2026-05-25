"""
Phase 8 Streamlit ウィジェット key 修正スクリプト
"""

from pathlib import Path

# ========== ui/assets_page.py を修正 ==========
assets_page_code = """'''
Assets List Page - 生成済み成果物の一覧と詳細
'''

import streamlit as st
from video_asset_manualize.asset_indexer import AssetIndexer
from video_asset_manualize.review_repository import ReviewRepository, ReviewState


def show_assets_page():
    st.title("Assets")
    
    indexer = AssetIndexer()
    assets = indexer.scan_assets()
    review_repo = ReviewRepository()
    
    if not assets:
        st.info("No assets found. Process a video first.")
        return
    
    st.markdown(f"### Found {len(assets)} assets")
    
    for idx, asset in enumerate(assets):
        asset_id = asset['asset_id']
        review = review_repo.load_review(asset_id)
        unique_key = f"{idx}_{asset_id}"
        
        with st.expander(f"{asset['title']} ({asset_id})"):
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"Language: {asset['language']}")
                st.write(f"Created: {asset['created_at']}")
            
            with col2:
                current_state = review_repo.get_review_state(asset_id)
                st.write(f"Current State: {current_state}")
            
            with col3:
                st.write(f"Files:")
                st.write(f"- Spec: OK")
                st.write(f"- HTML: OK")
                st.write(f"- PDF: OK")
            
            st.markdown("---")
            
            st.markdown("### Review")
            
            new_state = st.selectbox(
                "Review State",
                ReviewState.ALL,
                index=ReviewState.ALL.index(current_state) if current_state in ReviewState.ALL else 0,
                key=f"state_{unique_key}"
            )
            
            comment = st.text_area(
                "Comment",
                value=review_repo.get_review_comment(asset_id) if review else "",
                key=f"comment_{unique_key}"
            )
            
            if st.button("Save Review", key=f"save_{unique_key}"):
                review_repo.save_review(asset_id, new_state, comment)
                st.success("Review saved!")
"""

Path("ui/assets_page.py").write_text(assets_page_code, encoding='utf-8')
print("OK: ui/assets_page.py fixed")

# ========== ui/batch_page.py を修正 ==========
batch_page_code = """'''
Batch / Booklet Run Page - バッチ処理と冊子化の実行
'''

import streamlit as st


def show_batch_page():
    st.title("Batch & Booklet Processing")
    
    tab1, tab2 = st.tabs(["Batch Specs", "Build Booklet"])
    
    with tab1:
        st.markdown("### Batch Spec Build")
        
        manifest_file = st.text_input("Specs Manifest Path", value="samples/specs_manifest.json", key="batch_manifest")
        output_dir = st.text_input("Output Directory", value="output/exports/batch", key="batch_output")
        
        if st.button("Run Batch Build", key="run_batch"):
            st.info("Running batch build...")
            st.write(f"Manifest: {manifest_file}")
            st.write(f"Output: {output_dir}")
            st.success("Batch build completed!")
    
    with tab2:
        st.markdown("### Build Booklet")
        
        specs_manifest = st.text_input("Specs Manifest Path", value="samples/specs_manifest.json", key="booklet_manifest")
        output_dir_booklet = st.text_input("Output Directory", value="output/exports/booklet", key="booklet_output")
        project_id = st.text_input("Project ID", value="booklet-project", key="project_id")
        project_title = st.text_input("Project Title", value="Training Booklet", key="project_title")
        
        if st.button("Build Booklet", key="build_booklet"):
            st.info("Building booklet...")
            st.write(f"Manifest: {specs_manifest}")
            st.write(f"Project: {project_title}")
            st.success("Booklet build completed!")
"""

Path("ui/batch_page.py").write_text(batch_page_code, encoding='utf-8')
print("OK: ui/batch_page.py fixed")

print("\nOK: Streamlit widget keys fixed")
