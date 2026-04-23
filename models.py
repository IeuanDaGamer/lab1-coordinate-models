from dataclasses import dataclass
import math


@dataclass(frozen=True)
class CartesianPoint2D:
    x: float
    y: float

    @staticmethod
    def from_polar(polar_point: "PolarPoint") -> "CartesianPoint2D":
        x = polar_point.radius * math.cos(polar_point.angle)
        y = polar_point.radius * math.sin(polar_point.angle)
        return CartesianPoint2D(x, y)


@dataclass(frozen=True)
class PolarPoint:
    radius: float
    angle: float

    def __post_init__(self):
        if self.radius < 0:
            raise ValueError("Радіус не може бути від'ємним.")

    @staticmethod
    def from_cartesian(cartesian_point: CartesianPoint2D) -> "PolarPoint":
        radius = math.sqrt(cartesian_point.x ** 2 + cartesian_point.y ** 2)
        angle = math.atan2(cartesian_point.y, cartesian_point.x)
        return PolarPoint(radius, angle)


@dataclass(frozen=True)
class CartesianPoint3D:
    x: float
    y: float
    z: float

    @staticmethod
    def from_spherical(spherical_point: "SphericalPoint") -> "CartesianPoint3D":
        x = spherical_point.radius * math.sin(spherical_point.polar_angle) * math.cos(spherical_point.azimuth)
        y = spherical_point.radius * math.sin(spherical_point.polar_angle) * math.sin(spherical_point.azimuth)
        z = spherical_point.radius * math.cos(spherical_point.polar_angle)
        return CartesianPoint3D(x, y, z)


@dataclass(frozen=True)
class SphericalPoint:
    radius: float
    azimuth: float
    polar_angle: float

    def __post_init__(self):
        if self.radius < 0:
            raise ValueError("Радіус не може бути від'ємним.")

    @staticmethod
    def from_cartesian(cartesian_point: CartesianPoint3D) -> "SphericalPoint":
        x = cartesian_point.x
        y = cartesian_point.y
        z = cartesian_point.z

        radius = math.sqrt(x ** 2 + y ** 2 + z ** 2)

        if radius == 0:
            azimuth = 0.0
            polar_angle = 0.0
        else:
            azimuth = math.atan2(y, x)
            polar_angle = math.acos(z / radius)

        return SphericalPoint(radius, azimuth, polar_angle)