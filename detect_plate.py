# detect_plate.py

import os
import sys
import cv2
import torch
import numpy as np
from pathlib import Path

# Fix cross-platform issue: allow PosixPath unpickling on Windows
if sys.platform == "win32":
    import pathlib
    pathlib.PosixPath = pathlib.WindowsPath

# Add YOLOv5 directory to path
YOLO_ROOT = Path("D:/project/License Plate Recognition/yolov5").resolve()
sys.path.append(str(YOLO_ROOT))

from utils.general import non_max_suppression, scale_boxes
from utils.augmentations import letterbox
from models.common import DetectMultiBackend

def load_model(weights_path, device):
    model = DetectMultiBackend(weights_path, device=device)
    model.eval()
    return model

def preprocess_image(img, img_size):
    img0 = img.copy()
    img = letterbox(img, img_size, stride=32, auto=True)[0]
    img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR → RGB → 3xHxW
    img = np.ascontiguousarray(img)
    img = torch.from_numpy(img).float() / 255.0
    if img.ndimension() == 3:
        img = img.unsqueeze(0)
    return img, img0

def detect_plate(model, img0, device, img_size=640, conf_thres=0.25, iou_thres=0.45):
    img, original = preprocess_image(img0, img_size)
    img = img.to(device)

    with torch.no_grad():
        pred = model(img, augment=False, visualize=False)
        pred = non_max_suppression(pred, conf_thres, iou_thres)

    for det in pred:
        if det is not None and len(det):
            det[:, :4] = scale_boxes(img.shape[2:], det[:, :4], original.shape).round()
            for *xyxy, conf, cls in reversed(det):
                x1, y1, x2, y2 = map(int, xyxy)
                plate_img = img0[y1:y2, x1:x2]
                return plate_img, (x1, y1, x2, y2), conf.item()

    return None, None, None