import os
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

from constants import UPLOADED_SCREENSHOTS
from db import load_existing_trades, save_to_database, update_file_name_in_db, overwrite_database
from extraction import extract_text_from_image, parse_stock_actions, preprocess_image

os.makedirs(UPLOADED_SCREENSHOTS, exist_ok=True)

st.set_page_config(
    page_title="Stocks Extractor",
)

st.title("Stocks Extractor")


def re_extract_information():
    trades = []
    for file in os.listdir(UPLOADED_SCREENSHOTS):
        with open(os.path.join(UPLOADED_SCREENSHOTS, file), "rb") as f:
            file_bytes = f.read()
            preprocess_images = preprocess_image(file_bytes)
            text = extract_text_from_image(preprocess_images[-1])
            trades_df, matches, group_matches = parse_stock_actions(text)
            trades_df['file'] = file
            trades.append(trades_df)
    return pd.concat(trades, ignore_index=True)


# Filtering options
st.sidebar.header("Filter Options")
existing_trades = load_existing_trades()
print("existing_trades dtypes:", existing_trades.dtypes)
stock_filter = st.sidebar.text_input("Filter by Stock Name")
month_filter = st.sidebar.selectbox("Filter by Month", ["All"] + sorted(set(existing_trades["date"])) if not existing_trades.empty else ["All"])

uploaded_files = st.file_uploader("Upload trading screenshots", type=["jpg", "png", "jpeg"], accept_multiple_files=True)

if uploaded_files:
    trades = []
    for uploaded_file in uploaded_files:
        # Process uploaded file
        file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
        preprocess_images = preprocess_image(file_bytes)
        text = extract_text_from_image(preprocess_images[-1])
        trades_df, matches, group_matches = parse_stock_actions(text)
        trades.append(trades_df)

    # Display extracted trades
    st.subheader("Extracted Trades")
    trades_df = pd.concat(trades)
    st.dataframe(trades_df)

    # Save button
    if st.button("Save Trades"):
        trades_df["File"] = ""
        for uploaded_file in uploaded_files:
            # Save uploaded file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            file_path = os.path.join(UPLOADED_SCREENSHOTS, f"trade_{timestamp}.jpg")
            with open(file_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            trades_df.loc[trades_df["File"] == uploaded_file.name, "File"] = file_path
        save_to_database(trades_df)
        st.success("Trades saved to DuckDB!")

    for uploaded_file in uploaded_files:
        st.text("Screenshot")
        st.image(uploaded_file, use_container_width=True)

# Show existing trades from the database
st.subheader("Existing Trades in Database")

# Apply filters
if not existing_trades.empty:
    if stock_filter:
        existing_trades = existing_trades[existing_trades["stock"].str.contains(stock_filter, case=False, na=False)]
    if month_filter and month_filter != "All":
        existing_trades = existing_trades[existing_trades["date"] == month_filter]

st.data_editor(existing_trades)

# Button to re-extract information from files
if st.button("Re-extract Information") or "re_df" in st.session_state:
    df = re_extract_information()
    st.session_state['re_df'] = df
    st.success("Information re-extracted.")
    st.dataframe(df)

if "re_df" in st.session_state:
    if st.button("Over-write Database"):
        overwrite_database(st.session_state['re_df'])
        st.success("Trades we successfully over-written.")
