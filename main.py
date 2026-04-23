import math
from models import CartesianPoint2D, PolarPoint, CartesianPoint3D, SphericalPoint
from distances import (
    distance_2d_cartesian,
    distance_2d_polar,
    distance_3d_cartesian,
    distance_3d_spherical_chord,
    distance_3d_spherical_arc,
)
from benchmark import generate_2d_data, generate_3d_data, benchmark_2d, benchmark_3d


def almost_equal(a: float, b: float, eps: float = 1e-9) -> bool:
    return abs(a - b) < eps


def test_2d_conversions():
    print("=== Перевірка 2D перетворень ===")

    original_cart = CartesianPoint2D(3.0, 4.0)
    polar = PolarPoint.from_cartesian(original_cart)
    restored_cart = CartesianPoint2D.from_polar(polar)

    print("Початкова декартова точка:", original_cart)
    print("Перетворення у полярну:", polar)
    print("Зворотне перетворення у декартову:", restored_cart)

    print("X збігається:", almost_equal(original_cart.x, restored_cart.x))
    print("Y збігається:", almost_equal(original_cart.y, restored_cart.y))
    print()


def test_3d_conversions():
    print("=== Перевірка 3D перетворень ===")

    original_cart = CartesianPoint3D(3.0, 4.0, 5.0)
    spherical = SphericalPoint.from_cartesian(original_cart)
    restored_cart = CartesianPoint3D.from_spherical(spherical)

    print("Початкова декартова точка:", original_cart)
    print("Перетворення у сферичну:", spherical)
    print("Зворотне перетворення у декартову:", restored_cart)

    print("X збігається:", almost_equal(original_cart.x, restored_cart.x))
    print("Y збігається:", almost_equal(original_cart.y, restored_cart.y))
    print("Z збігається:", almost_equal(original_cart.z, restored_cart.z))
    print()


def test_distances():
    print("=== Перевірка відстаней ===")

    c1 = CartesianPoint2D(0.0, 0.0)
    c2 = CartesianPoint2D(3.0, 4.0)
    print("2D декартова відстань:", distance_2d_cartesian(c1, c2))

    p1 = PolarPoint.from_cartesian(c1)
    p2 = PolarPoint.from_cartesian(c2)
    print("2D полярна відстань:", distance_2d_polar(p1, p2))

    s1 = SphericalPoint(radius=10.0, azimuth=0.0, polar_angle=math.pi / 2)
    s2 = SphericalPoint(radius=10.0, azimuth=math.pi / 2, polar_angle=math.pi / 2)

    c3 = CartesianPoint3D.from_spherical(s1)
    c4 = CartesianPoint3D.from_spherical(s2)

    print("3D декартова відстань:", distance_3d_cartesian(c3, c4))
    print("3D сферична хорда:", distance_3d_spherical_chord(s1, s2))
    print("3D сферична дуга:", distance_3d_spherical_arc(s1, s2))
    print()


def run_benchmarks():
    print("=== Бенчмарки ===")

    n = 100000

    print(f"Генерація {n} пар 2D точок...")
    polar_pairs, cartesian_pairs_2d = generate_2d_data(n)
    polar_time, cart_time_2d, total_a, total_b = benchmark_2d(polar_pairs, cartesian_pairs_2d)

    print(f"2D Polar distance time: {polar_time:.6f} s")
    print(f"2D Cartesian distance time: {cart_time_2d:.6f} s")
    print(f"Контрольні суми: {total_a:.3f}, {total_b:.3f}")
    print()

    print(f"Генерація {n} пар 3D точок...")
    spherical_pairs, cartesian_pairs_3d = generate_3d_data(n)
    chord_time, arc_time, cart_time_3d, total_c, total_d, total_e = benchmark_3d(
        spherical_pairs, cartesian_pairs_3d
    )

    print(f"3D Spherical chord time: {chord_time:.6f} s")
    print(f"3D Spherical arc time: {arc_time:.6f} s")
    print(f"3D Cartesian distance time: {cart_time_3d:.6f} s")
    print(f"Контрольні суми: {total_c:.3f}, {total_d:.3f}, {total_e:.3f}")
    print()


if __name__ == "__main__":
    test_2d_conversions()
    test_3d_conversions()
    test_distances()
    run_benchmarks()