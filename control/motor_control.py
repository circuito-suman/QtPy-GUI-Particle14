import time  

class MotorController:
    def __init__(self):
        self.current_position = (0.0, 0.0, 0.0)

    def move_to(self, point_3d):
        print(f"[MotorController] Moving to: X={point_3d.x:.2f}, Y={point_3d.y:.2f}, Z={point_3d.z:.2f}")
        time.sleep(0.5)  # Wait for half a second to simulate movement
        # Update the current position
        self.current_position = (point_3d.x, point_3d.y, point_3d.z)
        # Print that the motor has arrived
        print(f"[MotorController] Arrived at: X={point_3d.x:.2f}, Y={point_3d.y:.2f}, Z={point_3d.z:.2f}")

class DummyMotorController(MotorController):
    pass
