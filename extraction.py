import re

import cv2
import numpy as np
import pandas as pd
import pytesseract

from constants import REGEX, REGEX_GROUP


def preprocess_image(file_bytes):
    # Load the image
    img_cv = cv2.imdecode(np.frombuffer(file_bytes, np.uint8), cv2.IMREAD_COLOR)

    # Increase the size of the image
    scale_percent = 80  # Increase size by 150%
    width = int(img_cv.shape[1] * scale_percent / 100)
    height = int(img_cv.shape[0] * scale_percent / 100)
    dim = (width, height)
    img_resized = cv2.resize(img_cv, dim, interpolation=cv2.INTER_LINEAR)

    # Convert to grayscale
    gray = cv2.cvtColor(img_resized, cv2.COLOR_BGR2GRAY)

    # Apply thresholding
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Remove noise
    kernel = np.ones((1, 1), np.uint8)
    processed_img = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

    return img_cv, img_resized, gray, thresh, processed_img


def extract_text_from_image(file_bytes):
    text = pytesseract.image_to_string(file_bytes, config="--psm 4")
    return text


def parse_stock_actions(text, regex=REGEX, regex_group=REGEX_GROUP):
    # Extract dates
    group_matches = list(re.compile(regex_group).finditer(text))

    # Extract stock actions
    pattern = re.compile(regex, re.MULTILINE)
    matches = list(pattern.finditer(text))

    trades = []
    for match in matches:
        trade_data = {}

        for group_match in reversed(group_matches):
            if group_match.start() < match.start():
                trade_data = group_match.groupdict()
                break

        trade_data = {**match.groupdict(), **trade_data}
        trades.append(trade_data)

    trades_df = pd.DataFrame(trades)
    
    return trades_df, matches, group_matches
