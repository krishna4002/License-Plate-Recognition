# recognize_text.py

import easyocr
import cv2
import numpy as np

# Load once
reader = easyocr.Reader(['en'], gpu=False)

def recognize_plate_text(plate_img):
    """
    Apply OCR to recognize text from a cropped license plate image.
    """
    if plate_img is None or plate_img.size == 0:
        return "Plate not readable"

    # Convert to RGB for EasyOCR
    if len(plate_img.shape) == 2:
        plate_img = cv2.cvtColor(plate_img, cv2.COLOR_GRAY2RGB)
    elif plate_img.shape[2] == 1:
        plate_img = cv2.cvtColor(plate_img, cv2.COLOR_GRAY2RGB)
    else:
        plate_img = cv2.cvtColor(plate_img, cv2.COLOR_BGR2RGB)

    # OCR inference
    result = reader.readtext(plate_img, detail=1)

    if not result:
        return "No text found"

    # Sort detected segments left-to-right based on x-coordinate
    sorted_results = sorted(result, key=lambda x: x[0][0][0])

    # Extract and join text parts with a space
    spaced_text = " ".join([res[1] for res in sorted_results])

    return spaced_text