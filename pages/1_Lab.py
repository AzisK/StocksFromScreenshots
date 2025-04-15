import os

import streamlit as st

from constants import UPLOADED_SCREENSHOTS, REGEX, PATTERN_GROUP
from extraction import extract_text_from_image, parse_stock_actions, preprocess_image

st.title("Lab")

# Load a sample screenshot by default
sample_screenshot_path = "sample_screenshot/sample_screenshot.jpg"
if os.path.exists(sample_screenshot_path):
    with open(sample_screenshot_path, "rb") as f:
        sample_screenshot_bytes = f.read()
else:
    sample_screenshot_bytes = None

uploaded_file = st.file_uploader("Upload a screenshot", type=["jpg", "png", "jpeg"])
regex = st.text_area("Regex", REGEX, height=68)
regex_group = st.text_area("Group regex", PATTERN_GROUP.pattern, height=68)

if uploaded_file is not None:
    file_bytes = uploaded_file.read()
else:
    file_bytes = sample_screenshot_bytes

if file_bytes is not None:
    preprocess_images = preprocess_image(file_bytes)

    # Extract text from image
    text = extract_text_from_image(preprocess_images[-1])

    trades_df, matches, group_matches = parse_stock_actions(text, regex, regex_group)

    # Display extracted stock actions
    st.subheader("Extracted Stocks")
    edited_trades_df = st.data_editor(trades_df)

    # Display save button
    save_button = st.button("Save")

    # Display matches
    with st.expander("Matches"):
        st.write(matches)
        for m in matches:
            st.write(m.groupdict())
    with st.expander("Group matches"):
        st.write(group_matches)
        for g in group_matches:
            st.write(g.groupdict())

    # Display extracted text
    st.subheader("Extracted Text")
    st.code(text, language="text")

    if save_button:
        # Save uploaded file
        file_path = os.path.join(UPLOADED_SCREENSHOTS, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(file_bytes)
        st.success(f"File saved as {uploaded_file.name}")

        # Save extracted data
        edited_trades_df.to_csv(os.path.join(UPLOADED_SCREENSHOTS, f"{uploaded_file.name}_trades.csv"), index=False)
        st.success("Extracted data saved")

    st.subheader("Screenshot")
    st.image(file_bytes, use_container_width=True)

    save_sample_button = st.button("Save Sample Screenshot")
    if save_sample_button:
        with open(sample_screenshot_path, "wb") as f:
            f.write(file_bytes)
        st.success(f"Sample screenshot saved as {sample_screenshot_path}")

    with st.expander("Preprocessed Images"):
        stage_titles = ["Resized", "Grayscale", "Thresholded", "Processed"]
        for img, title in zip(preprocess_images[1:], stage_titles):
            st.image(img, caption=title, use_container_width=True)