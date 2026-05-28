'''
Assets List Page - 生成済み成果物の一覧と詳細
'''

import streamlit as st
import json
from pathlib import Path
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
        
        spec_path = Path(f"output/exports/{asset_id}_spec.json")
        mode = "unknown"
        provider = "n/a"
        if spec_path.exists():
            try:
                with open(spec_path, "r", encoding="utf-8") as f:
                    spec_data = json.load(f)
                    mode = spec_data.get("metadata", {}).get("generation_mode", "unknown")
                    provider = spec_data.get("metadata", {}).get("provider", "n/a")
            except Exception:
                pass
                
        # Determine color for mode display
        if mode == "canonical":
            mode_color = "🟢"
        elif mode in ["fallback", "test"]:
            mode_color = "🟡"
        else:
            mode_color = "🔴"
            
        with st.expander(f"{mode_color} {asset['title']} ({asset_id})"):
            if mode == "canonical":
                st.success(f"**Generation Mode:** CANONICAL - Provider: {provider}")
            elif mode in ["fallback", "test"]:
                st.warning(f"**Generation Mode:** {mode.upper()} - ⚠️ 非正本 (Production-ready ではありません)")
            else:
                st.error(f"**Generation Mode:** UNKNOWN - ⚠️ 非 canonical spec")
                
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.write(f"Language: {asset['language']}")
                st.write(f"Created: {asset['created_at']}")
            
            with col2:
                current_state = review_repo.get_review_state(asset_id)
                st.write(f"Current State: {current_state}")
            
            with col3:
                st.markdown("<b>Files:</b>", unsafe_allow_html=True)
                
                dl_col1, dl_col2, dl_col3 = st.columns(3)
                
                # Spec
                if spec_path.exists():
                    with open(spec_path, "rb") as f:
                        dl_col1.download_button(label="📄 JSON", data=f, file_name=f"{asset_id}_spec.json", use_container_width=True, key=f"dl_spec_{unique_key}")
                else:
                    dl_col1.write("📄 N/A")
                
                # HTML
                html_path = Path(f"output/exports/{asset_id}_manual.html")
                if html_path.exists():
                    with open(html_path, "rb") as f:
                        dl_col2.download_button(label="🌐 HTML", data=f, file_name=f"{asset_id}_manual.html", mime="text/html", use_container_width=True, key=f"dl_html_{unique_key}")
                else:
                    dl_col2.write("🌐 N/A")
                
                # PDF
                pdf_path = Path(f"output/exports/{asset_id}_manual.pdf")
                if pdf_path.exists():
                    with open(pdf_path, "rb") as f:
                        dl_col3.download_button(label="📋 PDF", data=f, file_name=f"{asset_id}_manual.pdf", mime="application/pdf", use_container_width=True, key=f"dl_pdf_{unique_key}")
                else:
                    dl_col3.write("📋 N/A")
            
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
