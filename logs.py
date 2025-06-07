import csv
import os
from datetime import datetime

def save_plate_to_csv(text, source="image"):
    file_path = "detected_plates.csv"
    exists = os.path.isfile(file_path)

    with open(file_path, mode="a", newline='') as file:
        writer = csv.writer(file)
        if not exists:
            writer.writerow(["Timestamp", "Source", "LicensePlate"])
        writer.writerow([datetime.now().strftime("%Y-%m-%d %H:%M:%S"), source, text])