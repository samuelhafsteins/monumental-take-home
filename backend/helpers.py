import math

FRAMES = 30


def get_sign_and_abs(n: float):
    sign = 1
    if n < 0:
        sign = -1
    return sign, abs(n)


def dist_squared(x: float, y: float):
    return x**2 + y**2


def translate_radian(phi: float):
    return phi - (phi // (2 * math.pi)) * 2 * math.pi


def get_rotation_delta(phi_1: float, phi_2: float):
    phi_1, phi_2 = translate_radian(phi_1), translate_radian(phi_2)
    dphi_sign, dphi = get_sign_and_abs(phi_2 - phi_1)

    if dphi > math.pi:
        dphi = 2 * math.pi - dphi
        dphi_sign *= -1

    return dphi_sign * dphi
