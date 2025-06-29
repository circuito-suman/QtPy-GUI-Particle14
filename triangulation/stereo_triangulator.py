import numpy as np
from .point_3d import Point3D

class StereoTriangulator:
    def __init__(self, image_size=(640, 480), baseline=0.1):
        self.baseline = baseline # Distance between the two cameras in meters
        self.focal_length = self.calculate_focal_length(image_size)
        # Get the center of the image 
        self.image_center_x = image_size[0] // 2
        self.image_center_y = image_size[1] // 2

    def calculate_focal_length(self, image_size):
        width, height = image_size
        return max(width, height) * 1.2 # Rough estimate using trial and error

    def triangulate(self, point1, point2):
        x1, y1 = point1 # left camera point
        x2, y2 = point2 # right camera point
        disparity = abs(x1 - x2)
        if disparity < 1e-5:
            disparity = 1e-5
        #depth formula z = (focallength * baseline) / disparity
        z = (self.focal_length * self.baseline) / disparity
        #horizontal coordinates  formula x = ((x1 + x2) / 2 - image_center_x) * (z / focal_length)
        x = ((x1 + x2) / 2 - self.image_center_x) * (z / self.focal_length)
        #vertical coordinates formula y = ((y1 + y2) / 2 - image_center_y) * (z / focal_length)
        y = ((y1 + y2) / 2 - self.image_center_y) * (z / self.focal_length)
        return Point3D(x, y, z)
