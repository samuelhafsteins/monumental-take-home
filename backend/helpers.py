import math

FRAMES = 60


def get_sign_and_abs(n: float):
    sign = 1
    if n < 0:
        sign = -1
    return sign, abs(n)


def distance(x: float, y: float):
    return math.sqrt(x**2 + y**2)


def translate_radian(phi: float):
    return phi - (phi // (2 * math.pi)) * 2 * math.pi


def get_rotation_delta(phi_1: float, phi_2: float):
    phi_1, phi_2 = translate_radian(phi_1), translate_radian(phi_2)
    dphi_sign, dphi = get_sign_and_abs(phi_2 - phi_1)

    if dphi > math.pi:
        dphi = 2 * math.pi - dphi
        dphi_sign *= -1

    return dphi_sign * dphi


def closest_point_circle(cx: float, cz: float, px: float, pz: float, R: float):
    dx = px - cx
    dz = pz - cz

    # If the robot is standing in the desired postion
    # Add small number to avoid 0 division
    if dx == 0 and dz == 0:
        dx += 10**-3
        dz += 10**-3

    magD = distance(dx, dz)

    return cx + dx / magD * R, cz + dz / magD * R
