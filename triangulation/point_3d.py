class Point3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __str__(self):
        return f"Point3D(x={self.x:.2f}, y={self.y:.2f}, z={self.z:.2f})"
