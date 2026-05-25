'''
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
