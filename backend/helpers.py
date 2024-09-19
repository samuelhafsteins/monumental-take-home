FRAMES = 30

def get_sign_and_abs(n: float):
    sign = 1
    if n < 0:
        sign = -1
    return sign, abs(n)

def dist_squared(x: float, y: float):
    return x**2 + y**2