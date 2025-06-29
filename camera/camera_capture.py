import cv2  # Import OpenCV library for image and video processing

class CameraCapture:
    def __init__(self, source):
        self.cap = cv2.VideoCapture(source)
        if not self.cap.isOpened():
            raise ValueError(f"Could not open video source: {source}")

    def read_frame(self):
        # Read a frame (picture) from the camera/video
        ret, frame = self.cap.read()
        if not ret:
            return None
        return frame  

    def release(self):
        if self.cap.isOpened():
            self.cap.release()

    def get_resolution(self):
        width = int(self.cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        return (width, height)  
    # Return as a tuple  of (width, height)

    def get_fps(self):
        return self.cap.get(cv2.CAP_PROP_FPS)
