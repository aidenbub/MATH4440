import random

# Extended Euclidean Algorithm
def extended_euclidean(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x1, y1 = extended_euclidean(b % a, a)
        x = y1 - (b // a) * x1
        y = x1
        return gcd, x, y

# # Example EE usage
# a, b = 13, 17
# gcd, x, y = extended_euclidean(a, b)
# print(f"GCD: {gcd}")
# print(f"Coefficients: x = {x}, y = {y}")

# Modular inverse
def mod_inv(a, m):
    gcd, x, _ = extended_euclidean(a, m)
    if gcd != 1:
        return None  # Modular inverse does not exist
    else:
        return x % m
    
# Chinese Remainder Theorem
def chinese_remainder_theorem(congruences):
    total = 0
    M = 1
    for _, m in congruences:
        M *= m

    for a_i, m_i in congruences:
        M_i = M // m_i
        y_i = mod_inv(M_i, m_i)
        total += a_i * M_i * y_i

    return total % M

# # Example CRT usage
# congruences = [(2, 3), (3, 8)]
# x = chinese_remainder_theorem(congruences)
# print(f"The solution is: x = {x}")

# Elliptic Curve Factorization
# Point class
class Point:
    def __init__(self, x, y, infinity=False):
        self.x = x
        self.y = y
        self.infinity = infinity

    def __eq__(self, other):
        if self.infinity and other.infinity:
            return True
        if self.infinity or other.infinity:
            return False
        return self.x == other.x and self.y == other.y

    def __repr__(self):
        if self.infinity:
            return "Point(infinity)"
        return f"Point({self.x}, {self.y})"

# Point addition
def add_points(p1, p2, a, b, p):
    # Check for the point at infinity
    if p1.infinity:
        return p2
    if p2.infinity:
        return p1

    # Point doubling
    if p1 == p2:
        if p1.y == 0:  # Tangent is vertical
            return Point(None, None, True)  # Point at infinity
        inv = mod_inv(2 * p1.y, p)
        if inv is None:
            raise ValueError("Modular inverse does not exist")
        slope = (3 * p1.x**2 + a) * inv
    else:
        # Check if the line is vertical (points are inverses of each other)
        if p1.x == p2.x:
            return Point(None, None, True)  # Point at infinity
        inv = mod_inv(p2.x - p1.x, p)
        if inv is None:
            raise ValueError("Modular inverse does not exist")
        slope = (p2.y - p1.y) * inv
    
    x3 = (slope**2 - p1.x - p2.x) % p
    y3 = (slope * (p1.x - x3) - p1.y) % p

    return Point(x3, y3)

# # Example EC usage
# a, b, p = 2, 3, 97  # Curve parameters and prime modulus
# p1 = Point(3, 6)
# p2 = Point(3, 6)
# result = add_points(p1, p2, a, b, p)
# print(f"Result of adding {p1} and {p2} on the curve: {result}")

# Elliptic curve factorization
def elliptic_curve_factorization(n, max_iterations=1000):
    for _ in range(max_iterations):
        # Randomly choose curve parameters and a point
        a = random.randint(0, n-1)
        b = random.randint(0, n-1)
        x = random.randint(0, n-1)
        y = random.randint(0, n-1)

        curve = (a, b, n)  # y^2 = x^3 + ax + b (mod n)
        point = Point(x, y)

        try:
            for _ in range(1, max_iterations):
                # Attempt point doubling
                point = add_points(point, point, a, b, n)
        except ValueError:
            # A non-invertible element means we've potentially found a factor
            gcd, _, _ = extended_euclidean(point.x, n)
            if 1 < gcd < n:
                return gcd
    return None  # No factor found

# # Example EC factorization usage
# n = 589  # An integer to be factored
# factor = elliptic_curve_factorization(n)
# print(f"A non-trivial factor of {n} is: {factor}")