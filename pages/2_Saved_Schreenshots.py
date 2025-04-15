import os
import streamlit as st

from constants import UPLOADED_SCREENSHOTS

st.title("Saved Screenshots")

saved_files = os.listdir(UPLOADED_SCREENSHOTS)
for file in saved_files:
    file_path = os.path.join(UPLOADED_SCREENSHOTS, file)
    col1, col2 = st.columns([4, 1])
    with col1:
        st.image(file_path, caption=file, use_container_width=True)
    with col2:
        if st.button("Delete", key=file):
            os.remove(file_path)
