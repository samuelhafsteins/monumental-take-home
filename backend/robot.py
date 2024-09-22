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
    max_w: float = (math.pi / 4) / FRAMES
    a: float = (math.pi / 8) / FRAMES
    cutoff_phi: float = (math.pi / 4 + 0.1) / FRAMES

    destination_phi: float | None = None
    status_phi: Status = Status.STATIONARY

    def rotate(self, phi):
        self.status_phi = Status.MOVING
        self.destination_phi = phi

    def check_rotate(self):
        if self.status_phi == Status.MOVING:
            dest_phi = self.destination_phi
            dphi = get_rotation_delta(dest_phi, self.phi)

            if abs(dphi) <= self.cutoff_phi:
                self._reset_rotation()
                return True

            self.w += self.a
            self.w = min(self.max_w, self.w)

            if dphi < 0:
                self.phi += self.w
            else:
                self.phi -= self.w

            return True
        return False

    def _reset_rotation(self):
        self.w = 0
        self.status_phi = Status.STATIONARY
        self.destination_phi = None


class Crane(Rotation):
    y: float = 1.5

    v: float = 0
    max_v: float = 0.1 / FRAMES
    a: float = 0.02 / FRAMES
    cutoff: float = 0.11 / FRAMES

    destination_y: float | None = None
    status_y: Status = Status.STATIONARY

    def lift(self, y):
        self.status_y = Status.MOVING
        self.destination_y = y

    def check_lift(self):
        if self.status_y == Status.MOVING:
            dest_y = self.destination_y
            dy_sign, dy = get_sign_and_abs(dest_y - self.y)

            if dy <= self.cutoff:
                self._reset_lift()
                return True

            self.v += self.a
            self.v = min(self.max_v, self.v)

            self.y += dy_sign * self.v

            return True
        return False

    def _reset_lift(self):
        self.v = 0
        self.status_y = Status.STATIONARY
        self.destination_y = None


class Elbow(Rotation): ...


class Wrist(Rotation): ...


class Gripper(BaseModel):
    space: float = 0

    v: float = 0
    max_v: float = 0.03 / FRAMES
    a: float = 0.005 / FRAMES
    cutoff: float = 0.04 / FRAMES

    destination_open: float | None = None
    status_open: Status = Status.STATIONARY

    def open(self, space):
        self.status_open = Status.MOVING
        self.destination_open = space

    def check_open(self):
        if self.status_open == Status.MOVING:
            dest_open = self.destination_open
            dspace_sign, dspace = get_sign_and_abs(dest_open - self.space)

            if dspace <= self.cutoff:
                self._reset_open()
                return True

            self.v += self.a
            self.v = min(self.max_v, self.v)

            self.space += dspace_sign * self.v

            return True
        return False

    def _reset_open(self):
        self.v = 0
        self.destination_open = None
        self.status_open = Status.STATIONARY


class Robot(BaseModel):
    x: float = 0
    z: float = 0

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

    def move(self, x, z):
        self.status = Status.MOVING
        self.destination = (x, z)

    def _get_velocities(self, dx, dz):
        vx = math.sqrt(dx / (dx + dz)) * self.v
        vz = math.sqrt(dz / (dx + dz)) * self.v
        return (vx, vz)

    def check_move(self):
        if self.status == Status.MOVING:
            dest_x, dest_z = self.destination
            dx_sign, dx = get_sign_and_abs(dest_x - self.x)
            dz_sign, dz = get_sign_and_abs(dest_z - self.z)

            if dx + dz <= self.cutoff:
                # TODO nudge slow down and nudge closer
                self._reset_move()
                return True

            self.v += self.a
            self.v = min(self.max_v, self.v)

            vx, vz = self._get_velocities(dx, dz)
            self.x += dx_sign * vx
            self.z += dz_sign * vz

            return True
        return False

    def _reset_move(self):
        self.v = 0
        self.status = Status.STATIONARY
        self.destination = None

    def get_robot_data(self):
        return {
            "x": self.x,
            "z": self.z,
            "crane": {
                "phi": self.crane.phi,
                "y": self.crane.y,
            },
            "elbow": {
                "phi": self.elbow.phi,
            },
            "wrist": {
                "phi": self.wrist.phi,
            },
            "gripper": {
                "space": self.gripper.space,
            },
        }


robot = Robot()
