# app.py

import streamlit as st
import cv2
import tempfile
import numpy as np
from PIL import Image
import torch
from detect_plate import detect_plate, load_model
from recognize_text import recognize_plate_text
from logs import save_plate_to_csv

# Load model once at app start
YOLO_WEIGHTS = "yolov5/runs/train/lp_detector/weights/best.pt"
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
MODEL = load_model(YOLO_WEIGHTS, DEVICE)

st.set_page_config(page_title="License Plate Recognition", layout="centered")
st.title("🔍 License Plate Recognition System")

mode = st.sidebar.radio("Choose Mode", ["📸 Image", "📹 Video", "🟢 Real-Time Webcam"])

# --------------------- IMAGE ---------------------
if mode == "📸 Image":
    uploaded_file = st.file_uploader("Upload an image", type=["jpg", "jpeg", "png"])
    if uploaded_file:
        image = Image.open(uploaded_file).convert("RGB")
        img_np = np.array(image)

        plate_img, box, conf = detect_plate(MODEL, img_np, DEVICE)
        if plate_img is not None:
            x1, y1, x2, y2 = box
            cv2.rectangle(img_np, (x1, y1), (x2, y2), (0,255,0), 2)
            st.image(img_np, caption="Detected License Plate", use_column_width=True)

            text = recognize_plate_text(plate_img)
            st.success(f"Detected Plate Text: {text}")
            save_plate_to_csv(text, source="image")
        else:
            st.warning("No license plate detected.")

# --------------------- VIDEO ---------------------
elif mode == "📹 Video":
    uploaded_video = st.file_uploader("Upload a video", type=["mp4", "avi", "mov"])
    if uploaded_video:
        tfile = tempfile.NamedTemporaryFile(delete=False)
        tfile.write(uploaded_video.read())
        cap = cv2.VideoCapture(tfile.name)
        stframe = st.empty()

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            plate_img, box, conf = detect_plate(MODEL, frame, DEVICE)
            if plate_img is not None:
                x1, y1, x2, y2 = box
                text = recognize_plate_text(plate_img)
                save_plate_to_csv(text, source="video")
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            stframe.image(frame, channels="BGR", use_column_width=True)
        cap.release()

# --------------------- WEBCAM ---------------------
elif mode == "🟢 Real-Time Webcam":
    if st.button("Start Webcam"):
        cap = cv2.VideoCapture(0)
        stframe = st.empty()
        stop = st.button("Stop Webcam")
        while cap.isOpened() and not stop:
            ret, frame = cap.read()
            if not ret:
                break
            plate_img, box, conf = detect_plate(MODEL, frame, DEVICE)
            if plate_img is not None:
                x1, y1, x2, y2 = box
                text = recognize_plate_text(plate_img)
                save_plate_to_csv(text, source="webcam")
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0,255,0), 2)
                cv2.putText(frame, text, (x1, y1-10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (36,255,12), 2)
            stframe.image(frame, channels="BGR", use_container_width=True)
        cap.release()

# --------------------- CSV EXPORT ---------------------
if st.sidebar.button("📄 Download Detected Plates CSV"):
    try:
        with open("detected_plates.csv", "rb") as file:
            st.sidebar.download_button(
                label="Download CSV",
                data=file,
                file_name="detected_plates.csv",
                mime="text/csv"
            )
    except FileNotFoundError:
        st.sidebar.warning("No plates detected yet.")