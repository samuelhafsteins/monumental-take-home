from enum import StrEnum
from pydantic import BaseModel
import math
import json

from helpers import (
    FRAMES,
    closest_point_circle,
    get_sign_and_abs,
    get_rotation_delta,
    distance,
    translate_radian,
)

# All calculations will be done in SI units
# and will be calculated with respect to the frames


class Status(StrEnum):
    STATIONARY = "stationary"
    MOVING = "moving"


class Dimensions(BaseModel):
    width: float
    height: float
    depth: float


class RobotParts(BaseModel):
    body: Dimensions
    upper_arm: Dimensions
    lower_arm: Dimensions
    hand: Dimensions
    gripper: Dimensions


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

    # Boolean if to keep end-effector still
    destination: tuple[float, float, bool] | None = None

    status: Status = Status.STATIONARY

    parts: RobotParts

    def move(self, x, z, ef_still):
        self.status = Status.MOVING
        self.destination = (x, z, ef_still)

    def inverse_kinematic(self, x, y, z):
        # Inverse kinematic in respect to rotations
        _, _, wrist_x, wrist_z = self._get_position_of_joints()
        r = distance(wrist_x - self.x, wrist_z - self.z)
        desired_x, desired_z = closest_point_circle(x, z, self.x, self.z, r)

        # Have front of robot facing object
        alpha = math.atan2((x - desired_x), (z - desired_z))

        # Adjust to have gripper over object
        beta = self._get_angle_of_wrist_given_radius(r)

        theta = translate_radian(self.elbow.phi)
        if theta < math.pi:
            beta *= -1

        self.crane.lift(
            y
            + self.parts.upper_arm.height
            + self.parts.lower_arm.height
            + self.parts.hand.height
        )
        self.move(desired_x, desired_z, False)
        self.crane.rotate(alpha + beta)

    def check_move(self):
        if self.status == Status.MOVING:
            dest_x, dest_z, ef_still = self.destination

            self.v += self.a
            self.v = min(self.max_v, self.v)

            if ef_still:
                self._check_rotate_around_wrist(dest_x, dest_z)
            else:
                self._check_walk(dest_x, dest_z)

            return True
        return False

    def _check_walk(self, dest_x, dest_z):
        dx_sign, dx = get_sign_and_abs(dest_x - self.x)
        dz_sign, dz = get_sign_and_abs(dest_z - self.z)

        if distance(dx, dz) <= self.cutoff:
            self._reset_move()
            return

        vx, vz = self._get_velocities(dx, dz)
        self.x += dx_sign * vx
        self.z += dz_sign * vz

    def _check_rotate_around_wrist(self, dest_x, dest_z):
        # First move in a cycle to the angle of the destination
        _, _, wrist_x, wrist_z = self._get_position_of_joints()

        r = distance(wrist_x - self.x, wrist_z - self.z)

        cur_theta = math.atan2(self.x - wrist_x, self.z - wrist_z)
        dest_theta = math.atan2(dest_x - wrist_x, dest_z - wrist_z)

        d_theta = get_rotation_delta(dest_theta, cur_theta)

        if (
            distance(
                self.x - (wrist_x + r * math.sin(dest_theta)),
                self.z - (wrist_z + r * math.cos(dest_theta)),
            )
            < self.cutoff
        ):
            # Next move in a line to the position
            self._reset_move()

            dist_to_wrist = distance(wrist_x - dest_x, wrist_z - dest_z)
            upper_arm = self.parts.upper_arm.depth + self.parts.body.depth / 2
            try:
                # Rotation of elbow to desired length
                gamma = math.pi - math.acos(
                    (upper_arm**2 + self.parts.lower_arm.depth**2 - dist_to_wrist**2)
                    / (2 * self.parts.lower_arm.depth * upper_arm)
                )
            except ValueError:
                print(f"Arm cannot extend to desired length {dist_to_wrist}")
                return

            self.move(dest_x, dest_z, False)

            # Rotation of robot to keep grapper on point
            alpha = math.atan2((wrist_x - dest_x), (wrist_z - dest_z))
            beta = self._get_angle_of_wrist_given_radius(dist_to_wrist)

            self.elbow.rotate(gamma)

            # gamma is always positive, thus will always be on clockwise side
            self.crane.rotate(alpha - beta)
            return

        omega = self.v / r
        if d_theta > 0:
            omega *= -1

        self.x = wrist_x + r * math.sin(omega + cur_theta)
        self.z = wrist_z + r * math.cos(omega + cur_theta)

        # Small cheat here as there is no acceleration on rotation
        self.crane.phi += omega

    def _get_angle_of_wrist_given_radius(self, r):
        upper_arm = self.parts.upper_arm.depth + self.parts.body.depth / 2

        beta = math.acos(
            (r**2 + upper_arm**2 - self.parts.lower_arm.depth**2) / (2 * r * upper_arm)
        )

        return beta

    def _reset_move(self):
        self.v = 0
        self.status = Status.STATIONARY
        self.destination = None

    def _get_position_of_joints(self):
        elbow_x, elbow_z = self._get_elbow_pos()
        wrist_x, wrist_z = self._get_wrist_pos(elbow_x, elbow_z)

        return elbow_x, elbow_z, wrist_x, wrist_z

    def _get_velocities(self, dx, dz):
        vx = math.sqrt(dx / (dx + dz)) * self.v
        vz = math.sqrt(dz / (dx + dz)) * self.v
        return (vx, vz)

    def _get_elbow_pos(self):
        return (
            self.x
            + (self.parts.upper_arm.depth + self.parts.body.depth / 2)
            * math.sin(self.crane.phi),
            self.z
            + (self.parts.upper_arm.depth + self.parts.body.depth / 2)
            * math.cos(self.crane.phi),
        )

    def _get_wrist_pos(self, elbow_x, elbow_z):
        return (
            elbow_x
            + self.parts.lower_arm.depth * math.sin(self.elbow.phi + self.crane.phi),
            elbow_z
            + self.parts.lower_arm.depth * math.cos(self.elbow.phi + self.crane.phi),
        )

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


dimensions = {}

with open("robot_dimensions.json") as json_data:
    dimensions = json.load(json_data)

robot = Robot(parts=RobotParts.model_validate(dimensions["robot"]))
