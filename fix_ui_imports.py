"""
Phase 8 UI import パス修正スクリプト v2
"""

from pathlib import Path

# ========== ui/dashboard.py を修正 ==========
dashboard_code = """'''
Dashboard Page - プロジェクト概要と生成済み成果物
'''

import streamlit as st
from video_asset_manualize.asset_indexer import AssetIndexer
from video_asset_manualize.review_repository import ReviewRepository


def show_dashboard():
    st.title("Dashboard")
    
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
                    st.write(f"Language: {asset['language']}")
                    st.write(f"Created: {asset['created_at']}")
                
                with col2:
                    review_repo = ReviewRepository()
                    state = review_repo.get_review_state(asset['asset_id'])
                    st.write(f"Status: {state}")
                
                st.markdown("[View Spec](#) | [View HTML](#) | [View PDF](#)")
    
    if booklets:
        st.markdown("### Recent Booklets")
        
        for booklet in booklets[:3]:
            with st.expander(f"{booklet['title']} ({booklet['asset_count']} assets)"):
                st.write(f"Created: {booklet['created_at']}")
                st.markdown("[View HTML](#) | [View PDF](#)")
"""

Path("ui/dashboard.py").write_text(dashboard_code, encoding='utf-8')
print("OK: ui/dashboard.py updated")

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
    
    for asset in assets:
        asset_id = asset['asset_id']
        review = review_repo.load_review(asset_id)
        
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
print("OK: ui/assets_page.py updated")

print("\nOK: UI import paths fixed")
