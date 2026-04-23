import math
from models import CartesianPoint2D, PolarPoint, CartesianPoint3D, SphericalPoint


def distance_2d_cartesian(p1: CartesianPoint2D, p2: CartesianPoint2D) -> float:
    return math.sqrt((p2.x - p1.x) ** 2 + (p2.y - p1.y) ** 2)


def distance_2d_polar(p1: PolarPoint, p2: PolarPoint) -> float:
    return math.sqrt(
        p1.radius ** 2 + p2.radius ** 2 - 2 * p1.radius * p2.radius * math.cos(p2.angle - p1.angle)
    )


def distance_3d_cartesian(p1: CartesianPoint3D, p2: CartesianPoint3D) -> float:
    return math.sqrt(
        (p2.x - p1.x) ** 2 +
        (p2.y - p1.y) ** 2 +
        (p2.z - p1.z) ** 2
    )


def distance_3d_spherical_chord(p1: SphericalPoint, p2: SphericalPoint) -> float:
    cos_gamma = (
        math.sin(p1.polar_angle) * math.sin(p2.polar_angle) * math.cos(p1.azimuth - p2.azimuth)
        + math.cos(p1.polar_angle) * math.cos(p2.polar_angle)
    )

    value = p1.radius ** 2 + p2.radius ** 2 - 2 * p1.radius * p2.radius * cos_gamma
    return math.sqrt(max(value, 0.0))


def distance_3d_spherical_arc(p1: SphericalPoint, p2: SphericalPoint) -> float:
    if not math.isclose(p1.radius, p2.radius, rel_tol=1e-9, abs_tol=1e-9):
        raise ValueError("Для дугової відстані точки повинні лежати на одній сфері (мати однаковий радіус).")

    cos_gamma = (
        math.sin(p1.polar_angle) * math.sin(p2.polar_angle) * math.cos(p1.azimuth - p2.azimuth)
        + math.cos(p1.polar_angle) * math.cos(p2.polar_angle)
    )

    cos_gamma = max(-1.0, min(1.0, cos_gamma))
    gamma = math.acos(cos_gamma)

    return p1.radius * gamma