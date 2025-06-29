import cv2 
import numpy as np 
from ultralytics import YOLO 
from .detection_result import DetectionResult 

class ObjectDetector:
    def __init__(self, model_name='yolov8n.pt', target_classes=None, confidence_threshold=0.5, nms_threshold=0.4):
        self.model = YOLO(model_name)
        self.target_classes = target_classes 
        self.conf_thresh = confidence_threshold
        # ----Threshold for Non-Maximum Suppression (tend to remove overlapping boxes)
        self.nms_threshold = nms_threshold 

    def detect(self, frame):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.model(rgb_frame)
        
        # storage for all detections
        all_boxes = []
        all_confs = []
        all_cls_ids = []
        all_cls_names = []
        
        for result in results:
            boxes = result.boxes.xyxy.cpu().numpy()
            confs = result.boxes.conf.cpu().numpy()
            cls_ids = result.boxes.cls.cpu().numpy().astype(int)
            cls_names = [result.names[i] for i in cls_ids]
            
            for i in range(len(boxes)):
                # Only keep detections above the confidence threshold
                if confs[i] >= self.conf_thresh:
                    all_boxes.append(boxes[i])
                    all_confs.append(confs[i])
                    all_cls_ids.append(cls_ids[i])
                    all_cls_names.append(cls_names[i])
        
        # Convert bounding boxes to integer lists 
        boxes_list = [list(map(int, box)) for box in all_boxes]
        # Make a list of confidence scores as floats
        confidences_list = [float(conf) for conf in all_confs]
        
        # Using Non-Maximum Suppression to remove overlapping boxes
        indices = cv2.dnn.NMSBoxes(
            boxes_list, 
            confidences_list, 
            self.conf_thresh, 
            self.nms_threshold
        ) if boxes_list else np.array([], dtype=np.int32) 
        
        indices = indices.flatten() if isinstance(indices, np.ndarray) else np.array([], dtype=np.int32)
        
        detections = []
        for i in indices:
            x1, y1, x2, y2 = map(int, all_boxes[i])  # Box corners
            class_name = all_cls_names[i]
            
            if class_name in self.target_classes:
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                detections.append(DetectionResult(
                    class_name=class_name,
                    confidence=all_confs[i],
                    bbox=(x1, y1, x2, y2),
                    center=(center_x, center_y)
                ))
                
        return detections  
