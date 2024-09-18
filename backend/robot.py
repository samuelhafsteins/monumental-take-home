from pydantic import BaseModel

class Crane(BaseModel):
    z: float = 0
    phi: int = 0

class Elbow(BaseModel):
    phi: int = 0

class Wrist(BaseModel):
    phi: int = 0

class Gripper(BaseModel):
    space: int = 0

class Robot(BaseModel):
    x: float = 0
    y: float = 0

    crane: Crane = Crane()
    elbow: Elbow = Elbow()
    wrist: Wrist = Wrist()
    gripper: Gripper = Gripper()

    def move_robot(self, x, y):
        self.x = x
        self.y = y

        return (x, y)
    
    def rotate_crane(self, phi):
        self.crane.phi = phi

    def move_crane(self, z):
        self.crane.z = z

    def rotate_elbow(self, phi):
        self.elbow.phi = phi

    def rotate_wrist(self, phi):
        self.wrist.phi = phi
    
    def move_gripper(self, space):
        self.gripper.space = space

robot = Robot()
