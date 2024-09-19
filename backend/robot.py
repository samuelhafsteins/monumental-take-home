from enum import StrEnum
from pydantic import BaseModel
import math

from helpers import FRAMES, get_sign_and_abs

# All calculations will be done in SI units
# and will be calculated with respect to the frames

class Status(StrEnum):
    STATIONARY = "stationary"
    MOVING = "moving"
    STOP = "stop"

class RobotBase(BaseModel):
    status: Status = Status.STATIONARY

class Rotation(BaseModel):
    phi: float = 0

    w: float = 0
    max_w: float = math.pi / 2 / FRAMES
    a: float = math.pi / 4 / FRAMES


class Crane(RobotBase, Rotation):
    z: float = 0

    v: float = 0
    max_v: float = 0.01 / FRAMES
    a: float = 0.005 / FRAMES

    destination: tuple[float, float] | None = None

    def move(self, z, phi):
        self.status = Status.MOVING
        self.destination = (z, phi)

class Elbow(RobotBase, Rotation):
    destination: float | None = None

    def rotate(self, phi):
        self.status = Status.MOVING
        self.destination = phi


class Wrist(RobotBase, Rotation):
    destination: float | None = None

    def rotate(self, phi):
        self.status = Status.MOVING
        self.destination = phi

class Gripper(RobotBase):
    space: float = 0

    destination: float | None = None

    v: float = 0
    max_v: float = 0.01 / FRAMES
    a: float = 0.005 / FRAMES

    def move(self, space):
        self.status = Status.MOVING
        self.destination = space

class Robot(RobotBase):
    x: float = 0
    y: float = 0

    destination: tuple[float, float] | None = None

    crane: Crane = Crane()
    elbow: Elbow = Elbow()
    wrist: Wrist = Wrist()
    gripper: Gripper = Gripper()

    v: float = 0
    max_v: float = 3 / FRAMES
    a: float = 1 / FRAMES

    def move(self, x, y):
        self.status = Status.MOVING
        self.destination = (x, y)

    def _get_velocities(self, dx, dy):
        vx = math.sqrt(dx/(dx + dy)) * self.v
        vy = math.sqrt(dy/(dx + dy)) * self.v
        return (vx, vy)

    def check_move(self):
        if self.status == Status.MOVING:
            dest_x, dest_y = self.destination
            dx_sign, dx = get_sign_and_abs(dest_x - self.x)
            dy_sign, dy = get_sign_and_abs(dest_y - self.y)

            self.v += self.a
            self.v = min(self.max_v, self.v)

            vx, vy = self._get_velocities(dx, dy)
            self.x += dx_sign * vx
            self.y += dy_sign * vy

            if dx + dy <= 0.3:
                self.status = Status.STATIONARY
                self.destination = None

            return True
        return False

    def get_robot_data(self):
        return {
            "x": self.x,
            "y": self.y,
            "crane": {
                "phi": self.crane.phi,
                "z": self.crane.z,
            },
            "elbow": {
                "phi": self.elbow.phi,
            },
            "wrist": {
                "phi": self.wrist.phi,
            },
            "gripper": {
                "phi": self.gripper.space
            }
        }


robot = Robot()
