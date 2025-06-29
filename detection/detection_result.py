class DetectionResult:
    def __init__(self, class_name, confidence, bbox, center):
        self.class_name = class_name
        self.confidence = confidence
        # --Bounding box:
        self.bbox = bbox
        self.center = center
