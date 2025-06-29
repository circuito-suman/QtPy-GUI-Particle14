import cv2
import numpy as np
import time
import logging
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QHBoxLayout
from PyQt5.QtGui import QImage, QPixmap

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("DualWindowTracker")

class MainWindow(QWidget):
    def __init__(self, camera1, camera2, detector, triangulator, motor_controller):
        super().__init__()
        self.camera1 = camera1
        self.camera2 = camera2
        self.detector = detector
        self.triangulator = triangulator
        self.motor_controller = motor_controller

        self.setWindowTitle('Dual Window Object Tracker')
        self.setGeometry(100, 100, 1600, 600)

        # UI setup
        self.label1 = QLabel()
        self.label1.setAlignment(Qt.AlignCenter)
        self.label1.setStyleSheet("border: 2px solid black;")
        self.label2 = QLabel()
        self.label2.setAlignment(Qt.AlignCenter)
        self.label2.setStyleSheet("border: 2px solid black;")
        self.status_label = QLabel("Initializing...")
        self.status_label.setAlignment(Qt.AlignCenter)
        self.status_label.setStyleSheet("font-size: 22px; color: #001f4d; font-weight: bold;")

        layout = QHBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        main_layout = QVBoxLayout()
        main_layout.addLayout(layout)
        main_layout.addWidget(self.status_label)
        self.setLayout(main_layout)

        # Processing
        self.last_processing_time = 0
        self.frame_counter = 0
        self.processing_times = []
        self.target_fps = 30
        self.frame_skip = 1

        # Timer for frame updates
        self.timer = QTimer()
        self.timer.timeout.connect(self.process_frames)
        self.timer.start(1)  # As fast as possible
        self.label1.setFixedSize(640, 480)
        self.label2.setFixedSize(640, 480)
        self.setFixedSize(1300, 500)

    def process_frames(self):
        start_time = time.time()
        self.frame_counter += 1
        if self.frame_counter % self.frame_skip != 0:
            return

        frame1 = self.camera1.read_frame()
        frame2 = self.camera2.read_frame()
        if frame1 is None or frame2 is None:
            return

        detections1 = self.detector.detect(frame1)
        detections2 = self.detector.detect(frame2)

        frame1 = self.draw_detections_vectorized(frame1, detections1)
        frame2 = self.draw_detections_vectorized(frame2, detections2)

        # Cross-view matching
        matches = self.match_detections(detections1, detections2)
        if matches:
            det1, det2 = matches[0]
            point_3d = self.triangulator.triangulate(det1.center, det2.center)
            self.status_label.setText(f"Target at {point_3d}")
            self.motor_controller.move_to(point_3d)
        else:
            self.status_label.setText("Target not found in both views")

        self.display_frame(self.label1, frame1)
        self.display_frame(self.label2, frame2)

        processing_time = time.time() - start_time
        self.processing_times.append(processing_time)
        if len(self.processing_times) >= 30:
            avg_time = sum(self.processing_times) / len(self.processing_times)
            fps = 1 / avg_time if avg_time > 0 else 0
            logger.info(f"Avg processing: {avg_time:.4f}s | FPS: {fps:.1f}")
            self.processing_times = []

    def draw_detections_vectorized(self, frame, detections):
        if not detections:
            return frame
        img = frame.copy()
        for det in detections:
            x1, y1, x2, y2 = det.bbox
            img[y1:y2, x1:x2] = cv2.addWeighted(
                img[y1:y2, x1:x2], 0.7,
                np.full((y2 - y1, x2 - x1, 3), [0, 255, 0], dtype=np.uint8), 0.3, 0
            )
            label = f"{det.class_name} {det.confidence:.2f}"
            cv2.putText(img, label, (x1, y1 - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        return img

    def match_detections(self, detections1, detections2, max_distance=100):
        matches = []
        for det1 in detections1:
            if det1.class_name not in self.detector.target_classes:
                continue
            for det2 in detections2:
                if det1.class_name == det2.class_name:
                    dist = np.linalg.norm(np.array(det1.center) - np.array(det2.center))
                    if dist < max_distance:
                        matches.append((det1, det2))
        return matches

    def display_frame(self, label, frame):
       if frame is None or frame.size == 0:
          return
       frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
       h, w, ch = frame_rgb.shape
       bytes_per_line = ch * w
       q_img = QImage(frame_rgb.data, w, h, bytes_per_line, QImage.Format_RGB888)
       pixmap = QPixmap.fromImage(q_img).scaled(
        label.width(), label.height(), Qt.KeepAspectRatio, Qt.SmoothTransformation
       )  
       label.setPixmap(pixmap)


    def closeEvent(self, event):
        self.camera1.release()
        self.camera2.release()
        event.accept()
