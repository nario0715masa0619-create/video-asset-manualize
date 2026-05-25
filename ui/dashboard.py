'''
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
