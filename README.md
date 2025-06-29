# Dual Camera Object Tracker

This project is a modular Python application for dual-camera object tracking using PyQt5 for the GUI and YOLOv8 for object detection. It demonstrates stereo vision, object detection, cross-view matching, and simulated motion control. The application is designed for easy experimentation with video files or live webcams.

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/circuito-suman/QtPy-GUI-Particle14.git
cd QtPy-GUI-Particle14
```

### 2. Set Up Python Virtual Environment

A pre-configured virtual environment is provided in the `gta` folder.  
If you want to create your own, run:

```bash
python3 -m venv gta
source gta/bin/activate
```

### 3. Install Required Packages

Make sure you have the following system packages (for Ubuntu/Debian):

```bash
sudo apt-get update
sudo apt-get install python3-pyqt5 python3-opencv libxcb-xinerama0 libsm6 libxext6 libxrender1
```

Then install Python dependencies:

```bash
pip install pyqt5 opencv-python ultralytics numpy
```

### 4. Download YOLOv8 Model

Download the YOLOv8 model weights (e.g., `yolov8s.pt`) from [Ultralytics YOLOv8 releases](https://github.com/ultralytics/ultralytics/releases) and place it in the project root.

### 5. Run the Application

```bash
python3 start.py
```

---

## File Structure

```
QtPy-GUI-Particle14/
├── camera/
│   ├── __init__.py
│   └── camera_capture.py
├── control/
│   ├── __init__.py
│   └── motor_control.py
├── detection/
│   ├── __init__.py
│   ├── detection_result.py
│   └── object_detector.py
├── triangulation/
│   ├── __init__.py
│   ├── point_3d.py
│   └── stereo_triangulator.py
├── ui/
│   ├── __init__.py
│   └── mainwindow.py
├── gta/                # Python virtual environment (venv)
├── Recording/          # Example video files for testing
│   └── Screencast From 2025-06-29 23-00-08.mp4
├── start.py            # Main entry point
└── README.md
```

---

## Usage

- By default, the application uses sample video files for both camera feeds.
- To use your laptop's webcam(s), change the source in `start.py`:
  ```python
  camera1 = CameraCapture(0)  # Internal webcam
  camera2 = CameraCapture(1)  # External webcam or second camera
  ```
- You can also use your own video files by providing the file paths.

---

## Features

- Dual camera (or video) display in a PyQt5 GUI.
- Object detection using YOLOv8 (configurable for different classes).
- Cross-view matching and simple stereo triangulation for 3D position estimation.
- Simulated motor controller that logs movement commands.
- Modular code structure for easy extension and experimentation.

---

## Linux System Requirements

- Python 3.8 or newer
- PyQt5
- OpenCV (opencv-python)
- Numpy
- Ultralytics YOLOv8 (`ultralytics`)
- System libraries: `libxcb-xinerama0`, `libsm6`, `libxext6`, `libxrender1`

---

## Troubleshooting

- If you see errors about missing Qt platform plugins (`xcb`), make sure all required system libraries are installed.
- If the camera does not open, check that your webcam is connected and not used by another application.
- For best detection results, use a well-lit environment and a larger YOLO model (e.g., `yolov8m.pt`).

---

## Function Descriptions (User-Defined Modules)

### camera/camera_capture.py

- **CameraCapture(source):**  
  Opens a video file or camera device for frame capture.
- **read_frame():**  
  Returns the next frame from the video/camera.
- **get_resolution():**  
  Returns the width and height of the video stream.
- **release():**  
  Releases the video/camera resource.

### detection/object_detector.py

- **ObjectDetector:**  
  Loads a YOLOv8 model and provides detection on frames.
- **detect(frame):**  
  Returns a list of detected objects (bounding boxes, class, confidence).

### detection/detection_result.py

- **DetectionResult:**  
  Stores information about a single detection (bounding box, class, confidence, center).

### triangulation/stereo_triangulator.py

- **StereoTriangulator:**  
  Simulates stereo triangulation to estimate 3D coordinates from two camera views.
- **triangulate(center1, center2):**  
  Returns the estimated 3D position of the detected object.

### control/motor_control.py

- **MotorController:**  
  Simulates a motor controller for moving to a 3D point.
- **move_to(point_3d):**  
  Logs the movement command and updates the simulated position.

### ui/mainwindow.py

- **MainWindow:**  
  The main PyQt5 window that displays both video feeds, detection results, and status.
- **process_frames():**  
  Periodically grabs frames, runs detection, matches objects, and updates the GUI.
- **draw_detections_vectorized(frame, detections):**  
  Draws bounding boxes and labels on the frame.
- **match_detections(detections1, detections2):**  
  Matches detected objects between the two camera views.
- **display_frame(label, frame):**  
  Converts and displays a frame in a QLabel.

---

## Reference

- The `Recording` folder contains example video files for testing and demonstration.

---

## Customization

- To change the detected object, edit the `target_classes` in `start.py`.
- To adjust detection speed or accuracy, use a different YOLOv8 model and modify the confidence threshold.

---
