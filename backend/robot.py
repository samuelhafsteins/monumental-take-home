from enum import StrEnum
from pydantic import BaseModel
import math

from helpers import FRAMES, get_sign_and_abs, get_rotation_delta

# All calculations will be done in SI units
# and will be calculated with respect to the frames


class Status(StrEnum):
    STATIONARY = "stationary"
    MOVING = "moving"
    STOP = "stop"


class Rotation(BaseModel):
    phi: float = 0

    w: float = 0
    max_w: float = math.pi / 4 / FRAMES
    a: float = math.pi / 8 / FRAMES

    cutoff: float = (math.pi / 4 + 0.1) / FRAMES

    destination_phi: float | None = None
    status_phi: Status = Status.STATIONARY

    def rotate(self, phi):
        self.status_phi = Status.MOVING
        self.destination_phi = phi

    def check_rotate(self):
        if self.status_phi == Status.MOVING:
            dest_phi = self.destination_phi
            dphi = get_rotation_delta(dest_phi, self.phi)

            if abs(dphi) <= self.cutoff:
                self._reset_move()
                return True

            self.w += self.a
            self.w = min(self.max_w, self.w)

            if dphi < 0:
                self.phi += self.w
            else:
                self.phi -= self.w

            return True
        return False

    def _reset_move(self):
        self.w = 0
        self.status_phi = Status.STATIONARY
        self.destination_phi = None


class Crane(Rotation): ...


class Elbow(Rotation):
    z: float = 0.5

    v: float = 0
    max_v: float = 0.1 / FRAMES
    a: float = 0.02 / FRAMES

    destination_z: float | None = None
    status_z: Status = Status.STATIONARY
    cutoff: float = 0.11 / FRAMES

    def move(self, z):
        self.status_z = Status.MOVING
        self.destination_z = z

    def check_move(self):
        if self.status_z == Status.MOVING:
            dest_z = self.destination_z
            dz_sign, dz = get_sign_and_abs(dest_z - self.z)

            if dz <= self.cutoff:
                self.status_z = Status.STATIONARY
                self.destination_z = None
                return True

            self.v += self.a
            self.v = min(self.max_v, self.v)

            self.z += dz_sign * self.v

            return True
        return False


class Wrist(Rotation): ...


class Gripper(Rotation):
    space: float = 0

    v: float = 0
    max_v: float = 0.01 / FRAMES
    a: float = 0.005 / FRAMES

    destination: float | None = None

    def move(self, space):
        self.status = Status.MOVING
        self.destination = space


class Robot(Rotation):
    x: float = 0
    y: float = 0

    crane: Crane = Crane()
    elbow: Elbow = Elbow()
    wrist: Wrist = Wrist()
    gripper: Gripper = Gripper()

    v: float = 0
    max_v: float = 3 / FRAMES
    a: float = 1 / FRAMES
    cutoff: float = 3.1 / FRAMES

    destination: tuple[float, float] | None = None
    status: Status = Status.STATIONARY

    def move(self, x, y):
        self.status = Status.MOVING
        self.destination = (x, y)

    def _get_velocities(self, dx, dy):
        vx = math.sqrt(dx / (dx + dy)) * self.v
        vy = math.sqrt(dy / (dx + dy)) * self.v
        return (vx, vy)

    def check_move(self):
        if self.status == Status.MOVING:
            dest_x, dest_y = self.destination
            dx_sign, dx = get_sign_and_abs(dest_x - self.x)
            dy_sign, dy = get_sign_and_abs(dest_y - self.y)

            if dx + dy <= self.cutoff:
                # TODO nudge slow down and nudge closer
                self.status = Status.STATIONARY
                self.destination = None
                return True

            self.v += self.a
            self.v = min(self.max_v, self.v)

            vx, vy = self._get_velocities(dx, dy)
            self.x += dx_sign * vx
            self.y += dy_sign * vy

            return True
        return False

    def get_robot_data(self):
        return {
            "x": self.x,
            "y": self.y,
            "crane": {
                "phi": self.crane.phi,
            },
            "elbow": {
                "phi": self.elbow.phi,
                "z": self.elbow.z,
            },
            "wrist": {
                "phi": self.wrist.phi,
            },
            "gripper": {"phi": self.gripper.space},
        }


robot = Robot()
