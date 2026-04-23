import math
import random
import time
from models import PolarPoint, CartesianPoint2D, SphericalPoint, CartesianPoint3D
from distances import (
    distance_2d_polar,
    distance_2d_cartesian,
    distance_3d_spherical_chord,
    distance_3d_spherical_arc,
    distance_3d_cartesian,
)


def generate_2d_data(n: int):
    polar_pairs = []
    cartesian_pairs = []

    for _ in range(n):
        p1 = PolarPoint(
            radius=random.uniform(1.0, 1000.0),
            angle=random.uniform(0.0, 2 * math.pi)
        )
        p2 = PolarPoint(
            radius=random.uniform(1.0, 1000.0),
            angle=random.uniform(0.0, 2 * math.pi)
        )

        polar_pairs.append((p1, p2))

        c1 = CartesianPoint2D.from_polar(p1)
        c2 = CartesianPoint2D.from_polar(p2)
        cartesian_pairs.append((c1, c2))

    return polar_pairs, cartesian_pairs


def generate_3d_data(n: int):
    spherical_pairs = []
    cartesian_pairs = []

    for _ in range(n):
        radius = random.uniform(1.0, 1000.0)

        p1 = SphericalPoint(
            radius=radius,
            azimuth=random.uniform(0.0, 2 * math.pi),
            polar_angle=random.uniform(0.0, math.pi)
        )
        p2 = SphericalPoint(
            radius=radius,
            azimuth=random.uniform(0.0, 2 * math.pi),
            polar_angle=random.uniform(0.0, math.pi)
        )

        spherical_pairs.append((p1, p2))

        c1 = CartesianPoint3D.from_spherical(p1)
        c2 = CartesianPoint3D.from_spherical(p2)
        cartesian_pairs.append((c1, c2))

    return spherical_pairs, cartesian_pairs


def benchmark_2d(polar_pairs, cartesian_pairs):
    start = time.perf_counter()
    total_a = 0.0
    for p1, p2 in polar_pairs:
        total_a += distance_2d_polar(p1, p2)
    polar_time = time.perf_counter() - start

    start = time.perf_counter()
    total_b = 0.0
    for p1, p2 in cartesian_pairs:
        total_b += distance_2d_cartesian(p1, p2)
    cartesian_time = time.perf_counter() - start

    return polar_time, cartesian_time, total_a, total_b


def benchmark_3d(spherical_pairs, cartesian_pairs):
    start = time.perf_counter()
    total_a = 0.0
    for p1, p2 in spherical_pairs:
        total_a += distance_3d_spherical_chord(p1, p2)
    spherical_chord_time = time.perf_counter() - start

    start = time.perf_counter()
    total_b = 0.0
    for p1, p2 in spherical_pairs:
        total_b += distance_3d_spherical_arc(p1, p2)
    spherical_arc_time = time.perf_counter() - start

    start = time.perf_counter()
    total_c = 0.0
    for p1, p2 in cartesian_pairs:
        total_c += distance_3d_cartesian(p1, p2)
    cartesian_time = time.perf_counter() - start

    return spherical_chord_time, spherical_arc_time, cartesian_time, total_a, total_b, total_c