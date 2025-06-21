# 🚘 License-Plate-Recognition

This is a **real-time AI-based application** built to **detect and recognize license plates** from images, uploaded videos, or a live webcam feed.

It uses:

* **YOLOv5** for detecting license plates,
* **EasyOCR** to extract text from detected plates,
* **Streamlit** for a simple and clean interactive user interface.

> This project can be used for traffic analysis, smart parking, toll booth automation, and vehicle monitoring in cities.

---

## Key Features

* **Accurate License Plate Detection** using YOLOv5 trained on Indian plates via Roboflow
* **Text Recognition (OCR)** using EasyOCR to read plate numbers
* **Image Mode** — upload and process static images
* **Video Mode** — upload full videos and process all frames
* **Real-Time Webcam Mode** — detect license plates live from your webcam
* **Plate Logging** — every detected number plate is saved in a CSV file
* **CSV Export** — one-click download of recognized plate logs
* **Works Offline** — once models are downloaded, you don’t need internet access to run detections

---

## Project Structure

```bash
License Plate Recognition/
│
├── app.py                       # Main Streamlit UI
├── detect_plate.py              # YOLOv5-based plate detection logic
├── recognize_text.py            # EasyOCR-based plate text extraction
├── logs.py                      # Handles CSV writing of detected plates
├── detected_plates.csv          # Output log file of all recognized plates
│
├── yolov5/                      # Cloned YOLOv5 repository with model files
│   └── runs/train/...           # Includes the trained weights (best.pt)
│
├── requirements.txt             # Required Python libraries
└── model_training_prog.ipynb    # model training code on kaggle
```

---

## Installation & Setup Guide

### 1. Clone the Repo and Install Dependencies

```bash
git clone https://github.com/your-username/License-Plate-Recognition
cd License-Plate-Recognition
pip install -r requirements.txt
```

### 2. Clone the YOLOv5 GitHub Repo

```bash
git clone https://github.com/ultralytics/yolov5
```

Make sure it's inside your project folder.

---

### 3. Download and Train or Use Pretrained Indian Dataset

Use Roboflow dataset for Indian license plates:

```python
from roboflow import Roboflow
rf = Roboflow(api_key="YOUR_API_KEY")
project = rf.workspace("roboflow-universe-projects").project("license-plate-recognition-rxg4e")
dataset = project.version(11).download("yolov5")
```

You can either train the model or directly use the provided best.pt weight file after training.

---

### 4. Run the Streamlit App

```bash
streamlit run app.py
```

It will open an interactive UI in your browser.

---

## How the System Works

1. **Detection**: The detect_plate.py script loads the trained YOLOv5 model and detects license plates from input frames.
2. **Recognition**: The recognize_text.py script uses EasyOCR to extract readable text from the plate region.
3. **Logging**: All detected plate numbers, along with their input source (image/video/webcam), are saved to a CSV file for future tracking or analysis.
4. **UI Interaction**: Streamlit allows the user to easily choose modes, upload files, and view results in real-time.

---

## Sample Output (CSV Format)

| Plate Number | Source |
| ------------ | ------ |
| MH12AB1234   | image  |
| KA01CD5678   | video  |
| DL8CAF9988   | webcam |

---

## Use Cases

* **Law Enforcement**: Automate number plate checks and vehicle tracking.
* **Toll Booths**: Auto-recognition at entry/exit points.
* **Smart Parking**: Identify vehicles without human intervention.
* **Smart City Systems**: Monitor traffic and maintain real-time databases.
* **Surveillance**: Integrate with CCTV for automated alerts.

---

## Technologies Used

| Technology   | Purpose                                                 |
| ------------ | ------------------------------------------------------- |
| YOLOv5       | Real-time object detection (license plate bounding box) |
| EasyOCR      | Extracting text from the detected plates                |
| Streamlit    | Building interactive web UI                             |
| OpenCV       | Handling image/video capture and processing             |
| Roboflow     | Dataset access and model training                       |
| CSV          | Storing and exporting recognized plate text             |

---

## UI Modes at a Glance

* **Image Mode**
  Upload a single image and get the plate number.

* **Video Mode**
  Upload a full video file and extract plates from all frames.

* **Webcam Mode**
  Use your camera to detect license plates in real time.

---

## About This Project

This project was built to automate the detection and reading of *license plates* for smart city infrastructure. It's meant to be simple enough for beginners to use and powerful enough for real-time use cases like:

* Surveillance
* Gate automation
* Traffic enforcement
