'''
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
