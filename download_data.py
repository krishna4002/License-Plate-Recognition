#!pip install roboflow

from roboflow import Roboflow
rf = Roboflow(api_key="NvPiCMXIqZ6Uvw8244vQ")
project = rf.workspace("roboflow-universe-projects").project("license-plate-recognition-rxg4e")
version = project.version(11)
dataset = version.download("yolov5")