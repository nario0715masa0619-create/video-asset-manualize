'''
VideoAsset Manualize - Web UI Dashboard
'''

import streamlit as st
from pathlib import Path
import sys

# Add paths
base_dir = Path(__file__).parent
sys.path.insert(0, str(base_dir / "src"))
sys.path.insert(0, str(base_dir))

from ui.dashboard import show_dashboard
from ui.single_video_page import show_single_video_page
from ui.assets_page import show_assets_page
from ui.batch_page import show_batch_page


def main():
    st.set_page_config(
        page_title="VideoAsset Manualize",
        page_icon="O",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    st.sidebar.title("VideoAsset Manualize")
    st.sidebar.markdown("---")
    
    page = st.sidebar.radio(
        "Navigation",
        [
            "Dashboard",
            "Single Video",
            "Assets",
            "Batch & Booklet"
        ]
    )
    
    st.sidebar.markdown("---")
    
    st.sidebar.markdown("### About")
    st.sidebar.info(
        "VideoAsset Manualize is a tool for generating training manuals "
        "from video files using AI-powered extraction and LLM processing."
    )
    
    if page == "Dashboard":
        show_dashboard()
    
    elif page == "Single Video":
        show_single_video_page()
    
    elif page == "Assets":
        show_assets_page()
    
    elif page == "Batch & Booklet":
        show_batch_page()


if __name__ == "__main__":
    main()
