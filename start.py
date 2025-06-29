import os
import sys
from camera.camera_capture import CameraCapture
from detection.object_detector import ObjectDetector
from triangulation.stereo_triangulator import StereoTriangulator
from control.motor_control import DummyMotorController
from ui.mainwindow import MainWindow
from PyQt5.QtWidgets import QApplication


def main():
    # Initialize camera captures
    camera1 = CameraCapture('/home/circuito/QtPy-GUI-Particle14/a.webm')
    camera2 = CameraCapture('/home/circuito/QtPy-GUI-Particle14/a.webm')

    width, height = camera1.get_resolution()

    detector = ObjectDetector(
        target_classes=['bottle', 'cell phone'],
        confidence_threshold=0.3
    )
    triangulator = StereoTriangulator(
        image_size=(width, height),
        baseline=0.15 
    )
    motor_controller = DummyMotorController()
    # Create the main application window
    app = QApplication(sys.argv)
    window = MainWindow(camera1, camera2, detector, triangulator, motor_controller)
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
